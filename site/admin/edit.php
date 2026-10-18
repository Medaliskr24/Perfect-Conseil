<?php
require __DIR__ . '/../inc/bootstrap.php';
require __DIR__ . '/_ui.php';
$u = require_login();
$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$art = null;
if ($id) { $st = db()->prepare('SELECT * FROM pc_articles WHERE id = ?'); $st->execute(array($id)); $art = $st->fetch(); if (!$art) fail(404, 'المقال غير موجود.'); }
$errs = array();
$f = $art ? array('title' => $art['title'], 'slug' => $art['slug'], 'category' => $art['category'], 'description' => $art['description'], 'published_at' => $art['published_at'], 'status' => $art['status'], 'body' => $art['body'])
          : array('title' => '', 'slug' => '', 'category' => '', 'description' => '', 'published_at' => gmdate('Y-m-d'), 'status' => 'published', 'body' => '');
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  csrf_check();
  if (isset($_POST['action']) && $_POST['action'] === 'delete' && $art) {
    delete_cover($art['cover']);
    db()->prepare('DELETE FROM pc_articles WHERE id = ?')->execute(array($art['id']));
    header('Location: index.php?m=deleted'); exit;
  }
  $f['title'] = trim((string)(isset($_POST['title']) ? $_POST['title'] : ''));
  $f['category'] = trim((string)(isset($_POST['category']) ? $_POST['category'] : '')) ?: 'Actualités';
  $f['description'] = trim((string)(isset($_POST['description']) ? $_POST['description'] : ''));
  $f['published_at'] = (string)(isset($_POST['published_at']) ? $_POST['published_at'] : '');
  $f['status'] = (isset($_POST['status']) && $_POST['status'] === 'draft') ? 'draft' : 'published';
  $f['slug'] = strtolower(trim((string)(isset($_POST['slug']) ? $_POST['slug'] : '')));
  if ($f['slug'] === '') $f['slug'] = slugify($f['title']);
  $f['body'] = sanitize_html((string)(isset($_POST['body']) ? $_POST['body'] : ''));
  $L = function ($s) { return mb_strlen($s, 'UTF-8'); };
  if ($L($f['title']) < 3 || $L($f['title']) > 190) $errs[] = 'العنوان مطلوب (3 إلى 190 حرفاً).';
  if ($L($f['category']) > 60) $errs[] = 'اسم الفئة طويل جداً.';
  if ($L($f['description']) < 20 || $L($f['description']) > 300) $errs[] = 'الوصف المختصر مطلوب (20 إلى 300 حرف).';
  if (!valid_date($f['published_at'])) $errs[] = 'التاريخ غير صالح.';
  if (!valid_slug($f['slug'])) $errs[] = 'رابط المقال (slug) غير صالح: أحرف لاتينية صغيرة وأرقام وشرطات فقط.';
  if (plain_len($f['body']) < 20) $errs[] = 'نص المقال قصير جداً.';
  if (!$errs) {
    $d = db()->prepare('SELECT id FROM pc_articles WHERE slug = ? AND id <> ?'); $d->execute(array($f['slug'], $art ? $art['id'] : 0));
    if ($d->fetch()) $errs[] = 'رابط المقال (slug) مستعمل من قبل.';
  }
  $cerr = '';
  $newCover = save_cover(isset($_FILES['cover']) ? $_FILES['cover'] : null, $cerr);
  if ($cerr) $errs[] = $cerr;
  if (!$errs) {
    $cover = $art ? $art['cover'] : null;
    if ($newCover) { delete_cover($cover); $cover = $newCover; }
    elseif (!empty($_POST['remove_cover'])) { delete_cover($cover); $cover = null; }
    if ($art) {
      db()->prepare('UPDATE pc_articles SET slug=?, title=?, category=?, description=?, body=?, cover=?, status=?, published_at=?, updated_at=UTC_TIMESTAMP() WHERE id=?')
        ->execute(array($f['slug'], $f['title'], $f['category'], $f['description'], $f['body'], $cover, $f['status'], $f['published_at'], $art['id']));
      $nid = (int)$art['id'];
    } else {
      db()->prepare('INSERT INTO pc_articles (slug, title, category, description, body, cover, status, published_at, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,UTC_TIMESTAMP(),UTC_TIMESTAMP())')
        ->execute(array($f['slug'], $f['title'], $f['category'], $f['description'], $f['body'], $cover, $f['status'], $f['published_at']));
      $nid = (int)db()->lastInsertId();
    }
    header('Location: edit.php?id=' . $nid . '&m=saved'); exit;
  } elseif ($newCover) { delete_cover($newCover); }
}
ui_head($art ? 'تعديل مقال' : 'مقال جديد', 'ad');
echo '<div class="app">'; ui_side($u, $art ? '' : 'new'); echo '<main>' . ui_flash();
if ($errs) { echo '<div class="al bad" role="alert"><ul>'; foreach ($errs as $x) echo '<li>' . e($x) . '</li>'; echo '</ul></div>'; }
echo '<form method="post" enctype="multipart/form-data" id="fm" class="g2">' . csrf_field() . '<section><h1>' . ($art ? 'تعديل المقال' : 'مقال جديد') . '</h1><div class="cd">'
 . '<label for="title">العنوان</label><input id="title" name="title" maxlength="190" required dir="auto" value="' . e($f['title']) . '"><span class="hint" id="tc"></span>'
 . '<div class="row"><div><label for="category">الفئة</label><input id="category" name="category" list="cl" maxlength="60" dir="auto" value="' . e($f['category']) . '"><datalist id="cl"><option>Normes</option><option>Sécurité alimentaire</option><option>Qualité</option><option>Réglementation</option><option>Actualités</option></datalist></div>'
 . '<div><label for="published_at">تاريخ النشر</label><input id="published_at" name="published_at" type="date" required value="' . e($f['published_at']) . '"></div>'
 . '<div><label for="status">الحالة</label><select id="status" name="status"><option value="published"' . ($f['status'] === 'published' ? ' selected' : '') . '>منشور</option><option value="draft"' . ($f['status'] === 'draft' ? ' selected' : '') . '>مسودة</option></select></div></div>'
 . '<label for="slug">رابط المقال (slug)</label><input id="slug" name="slug" maxlength="100" dir="ltr" value="' . e($f['slug']) . '" data-new="' . ($art ? '0' : '1') . '">'
 . '<label for="description">الوصف المختصر (يظهر في جوجل)</label><textarea id="description" name="description" rows="2" maxlength="300" dir="auto">' . e($f['description']) . '</textarea><span class="hint" id="xc"></span></div>'
 . '<div class="cd"><div class="tb" id="tb"></div><div id="ed" contenteditable="true" role="textbox" aria-multiline="true" aria-label="محتوى المقال" dir="auto">' . ($f['body'] !== '' ? $f['body'] : '<p dir="auto"><br></p>') . '</div><div id="pv"></div><textarea name="body" id="body" hidden></textarea><p class="hint" id="wc"></p></div></section>'
 . '<section class="side"><div class="cd"><h3>صورة الغلاف</h3>';
$curCover = $art && $art['cover'] ? $art['cover'] : '';
echo '<img id="cvp" alt="" ' . ($curCover ? 'src="../uploads/' . e($curCover) . '"' : 'class="hid"') . '>'
 . '<input type="file" name="cover" id="cf" accept="image/jpeg,image/png,image/webp" hidden><label class="b w c" for="cf">اختيار صورة</label>'
 . ($curCover ? '<label class="chk"><input type="checkbox" name="remove_cover" value="1"> حذف الصورة الحالية</label>' : '')
 . '<p class="hint">تُصغَّر وتُضغط تلقائياً إلى 1200×675 على الخادم.</p></div>'
 . '<div class="cd"><h3>جودة المقال (SEO)</h3><div class="bar"><i id="sb"></i></div><ul id="sl"></ul></div>'
 . '<div class="cd ac"><button class="b p" type="submit">حفظ</button><button class="b" type="button" id="pb">معاينة</button>'
 . ($art && $art['status'] === 'published' ? '<a class="b c" href="../actualites/' . e($art['slug']) . '.html" target="_blank" rel="noopener">عرض في الموقع ↗</a>' : '') . '</div></section></form>';
if ($art) echo '<form method="post" class="cd dz" id="df" data-confirm="هل تريد حذف هذا المقال نهائياً؟">' . csrf_field() . '<input type="hidden" name="action" value="delete"><button class="b d" type="submit">حذف المقال نهائياً</button></form>';
echo '</main></div>';
ui_end();
