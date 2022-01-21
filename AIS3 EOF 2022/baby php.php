<?php
// using php:7.4-apache Dokcer image
isset($_GET['8']) && ($_GET['8'] === '===D') && die(show_source(__FILE__, 1));

$dir = "sandbox/" . md5(session_start() . session_id());
if (!file_exists($dir)) mkdir($dir);
chdir($dir);

!isset($_GET['code']) && die('/?8====D');

$time = date('Y-m-d-H:i:s');

$out = ($_GET['output'] ?? "$time.html");

if (strlen($out) > 255) die('toooooooo loooooong');

$ext = pathinfo($out) ['extension'];
if (trim($ext) !== '' && strtolower(substr($ext, 0, 2)) !== "ph") {
    $template = file_get_contents('/var/www/html/template.html');
    file_put_contents($out, sprintf($template, $time, highlight_string($_GET['code'], true)));
} else die("BAD");

echo "<p>Highlight:
<a href=\"/$dir/$out\">$out</a></p>"
// You might also need: /phpinfo.php

?>