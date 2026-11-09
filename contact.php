<?php
/**
 * Stolz Consulting – Kontaktformular-Handler
 * Versendet die Anfrage per mail() an die unten hinterlegte Adresse.
 * Voraussetzung: PHP-Hosting mit funktionierendem Mailversand.
 */

header('Content-Type: application/json; charset=utf-8');

const RECIPIENT = 'office@stolz-consulting.net';
const FROM      = 'no-reply@stolz-consulting.net';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false]);
    exit;
}

// Honeypot gegen Spam-Bots
if (!empty($_POST['website'])) {
    echo json_encode(['ok' => true]);
    exit;
}

function field(string $key, int $max = 500): string {
    $v = trim((string)($_POST[$key] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
}

$name    = field('name', 120);
$company = field('company', 160);
$email   = field('email', 160);
$phone   = field('phone', 60);
$subject = field('subject', 160);
$message = field('message', 5000);
$consent = !empty($_POST['consent']);
$lang    = field('lang', 2) === 'en' ? 'en' : 'de';

if ($name === '' || $message === '' || !$consent || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['ok' => false]);
    exit;
}

// Header-Injection verhindern
$name    = str_replace("\n", ' ', $name);
$subject = str_replace("\n", ' ', $subject);

$mailSubject = 'Website-Anfrage' . ($subject !== '' ? ': ' . $subject : '') . ' (' . strtoupper($lang) . ')';

$body  = "Neue Anfrage über stolz-consulting.net\n\n";
$body .= "Name:        $name\n";
$body .= "Unternehmen: " . ($company !== '' ? $company : '-') . "\n";
$body .= "E-Mail:      $email\n";
$body .= "Telefon:     " . ($phone !== '' ? $phone : '-') . "\n";
$body .= "Betreff:     " . ($subject !== '' ? $subject : '-') . "\n\n";
$body .= "Nachricht:\n$message\n";

$headers = [
    'From: Stolz Consulting Website <' . FROM . '>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=utf-8',
    'X-Mailer: PHP/' . phpversion(),
];

$sent = mail(
    RECIPIENT,
    '=?UTF-8?B?' . base64_encode($mailSubject) . '?=',
    $body,
    implode("\r\n", $headers)
);

http_response_code($sent ? 200 : 500);
echo json_encode(['ok' => $sent]);
