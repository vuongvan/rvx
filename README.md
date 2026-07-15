# Obtainium Import Links – Auto Generator (bản .ini)

Tự động sinh `index.html` (trang link import Obtainium) từ file `config.ini`, xử lý bằng Python (chỉ dùng thư viện chuẩn, không cần `pip install` gì cả).

## Cấu trúc

- `config.ini` — nơi bạn khai báo app. Chỉ cần sửa file này.
- `generate.py` — đọc `config.ini`, xuất ra `index.html`.
- `.github/workflows/generate.yml` — mỗi khi push thay đổi vào `config.ini`, Action tự chạy `generate.py` và commit lại `index.html`.

## Format `config.ini`

Mỗi app là 1 section riêng, tên section tuỳ ý (không trùng nhau):

```ini
[GmsCore-Default]
group = GmsCore (microG)
label = Default
id = app.revanced.android.gms
url = https://github.com/ReVanced/GmsCore
author = ReVanced
name = GmsCore
versionDetection = false
apkFilterRegEx = ^[^hw]+$
```

- `group` — tên nhóm hiển thị (các app cùng `group` sẽ được gom vào chung 1 bảng, theo đúng thứ tự trong file).
- `label` — chữ hiển thị trên nút bấm.
- `id`, `url`, `author`, `name` — bắt buộc, giống hệt config Obtainium.
- Các key khác ngoài `group/label/id/url/author/name/preferredApkIndex/overrideSource` (ví dụ `versionDetection`, `apkFilterRegEx`, ...) sẽ **tự động** được gom vào `additionalSettings`.
- `true` / `false` sẽ tự chuyển thành boolean, số sẽ tự chuyển thành int.
- Muốn đổi tiêu đề trang, sửa ở section `[title]`:

```ini
[title]
page_title = Import Links cho Obtainium
```

## Chạy thử local

```bash
python generate.py config.ini index.html
```

## Thêm app mới

Copy 1 block section, đổi tên section (vd `[TenApp-Bien-The]`), sửa các giá trị, push lên `main`. Action tự regenerate `index.html`.

## Deploy GitHub Pages

Settings → Pages → chọn branch `main`, thư mục gốc (`/`). Sau khi Action commit `index.html`, trang sẽ tự cập nhật.

## Lưu ý

Link dùng đúng format đã xác nhận hoạt động: `https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/<json-encoded>` (không dùng `redirect.html`).
