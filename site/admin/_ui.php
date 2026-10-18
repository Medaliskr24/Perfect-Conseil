<?php
function ui_head($title, $cls = '') {
  admin_headers();
  echo '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>' . e($title) . ' – Perfect Conseil</title><link rel="icon" href="../favicon.png"><link rel="stylesheet" href="admin.css"></head><body class="' . e($cls) . '">';
}
function ui_side($u, $active) {
  echo '<aside><div class="bd"><img src="../img/logo.webp" alt="Perfect Conseil" width="190" height="42"><small>لوحة تحكم المقالات</small></div>'
    . '<a class="nv' . ($active === 'list' ? ' on' : '') . '" href="index.php">المقالات</a>'
    . '<a class="nv' . ($active === 'new' ? ' on' : '') . '" href="edit.php">+ مقال جديد</a>'
    . '<a class="nv' . ($active === 'acc' ? ' on' : '') . '" href="account.php">حسابي وكلمة السر</a>'
    . '<a class="nv" href="../index.html" target="_blank" rel="noopener">عرض الموقع ↗</a><div class="sp"></div>'
    . '<p class="who">' . e($u['email']) . '</p>'
    . '<form method="post" action="logout.php">' . csrf_field() . '<button class="b w" type="submit">تسجيل الخروج</button></form></aside>';
}
function ui_flash() {
  $m = isset($_GET['m']) ? $_GET['m'] : '';
  $t = array('saved' => 'تم الحفظ ✔', 'deleted' => 'تم حذف المقال.', 'pwd' => 'تم تغيير كلمة السر ✔');
  return isset($t[$m]) ? '<div class="al ok">' . e($t[$m]) . '</div>' : '';
}
function ui_end($js = 'admin.js') { echo '<script src="' . e($js) . '"></script></body></html>'; }
