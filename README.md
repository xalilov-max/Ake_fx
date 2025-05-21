# Ake.fx 🎯

**Ake.fx** — bu foydalanuvchilarga valyuta bozorini kuzatish, tahlil qilish va yangiliklardan xabardor bo‘lish imkonini beruvchi zamonaviy web ilova. Ushbu loyiha Django backend va zamonaviy frontend texnologiyalari (HTML, CSS, JavaScript) asosida ishlab chiqilgan.

---

## 📌 Loyiha Maqsadi

Ake.fx loyihasining asosiy maqsadi — foydalanuvchilarga **forex (valyuta almashinuvi) bozoridagi** real vaqt ma'lumotlarini taqdim etish, shuningdek foydalanuvchilarni bozor tahlillari, yangiliklar va prognozlar bilan ta'minlashdir.

---

## 🔧 Texnologiyalar

- **Python** (Django Framework) – backend uchun
- **HTML / CSS / JavaScript** – frontend
- **SQLite** – ma’lumotlar bazasi
- **Bootstrap** – interfeys dizayni va moslashuvchanlik
- **Django Auth** – foydalanuvchi ro‘yxatdan o‘tishi va kirish tizimi

---

## 📂 Loyiha Tuzilishi

- `akefx/` – asosiy Django ilovasi (valyuta bilan ishlovchi modullar)
- `users/` – foydalanuvchilarni ro‘yxatdan o‘tkazish va tizimga kiritish
- `templates/` – barcha HTML shablonlar
- `staticfiles/` – CSS, JavaScript va rasmlar
- `media/` – foydalanuvchi yuklagan fayllar
- `db.sqlite3` – loyihaning ma’lumotlar bazasi

---

## 🔐 Foydalanuvchi Funksiyalari

- Tizimda ro‘yxatdan o‘tish va login qilish
- Bozor statistikasi va kurslarni ko‘rish
- Yangiliklar bilan tanishish
- Valyuta tahlillarini o‘qish
- (Kelajakda) Shaxsiy profil, tahlil qo‘shish, grafiklar ko‘rish

---

## 🚀 Ishga Tushirish

```bash
git clone https://github.com/xalilov-max/Ake_fxdjango.git
cd Ake_fxdjango
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
