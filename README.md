# Ake.fx 🎯

**Ake.fx** — bu zamonaviy trading va ta’lim platformasi. Foydalanuvchilar kurslarga yozilishi, mentorlar bilan ishlashi, o‘z fikrini (sharh) qoldirishi, profilini boshqarishi va to‘lovlarni amalga oshirishi mumkin. Loyiha Django backend va zamonaviy frontend texnologiyalari asosida ishlab chiqilgan.

---

## 📌 Loyiha Maqsadi

Ake.fx foydalanuvchilarga **forex va trading** bo‘yicha sifatli kurslar, mentorlar va real tajribalarni taqdim etadi. Platforma orqali:
- Kurslarni ko‘rish va sotib olish
- Mentorlar bilan tanishish
- Kurslar bo‘yicha sharh va baho qoldirish
- Profil va buyurtmalarni boshqarish
- To‘lovlarni amalga oshirish
- Foydalanuvchi va admin uchun qulay boshqaruv

---

## 🔧 Texnologiyalar

- **Python** (Django Framework) – backend
- **HTML / CSS / JavaScript** – frontend
- **Bootstrap** – zamonaviy dizayn va responsive
- **SQLite** – standart ma’lumotlar bazasi (PostgreSQL yoki MySQL ham ishlatish mumkin)
- **Django Auth** – foydalanuvchi autentifikatsiyasi
- **AJAX** – interaktiv sharhlar va boshqa funksiyalar uchun
- **Django Admin** – admin panel

---

## 📂 Loyiha Tuzilishi

- `akefx/` – asosiy Django ilovasi (trading va ta’lim modullari)
- `users/` – foydalanuvchilarni ro‘yxatdan o‘tkazish va tizimga kiritish
- `courses/` – kurslar va ularning boshqaruvi
- `mentors/` – mentorlar bilan bog‘liq funksiyalar
- `orders/` – buyurtmalar va to‘lovlar
- `reviews/` – sharhlar va baholar
- `templates/` – barcha HTML shablonlar
- `staticfiles/` – CSS, JavaScript va rasmlar
- `media/` – foydalanuvchi yuklagan fayllar
- `db.sqlite3` – loyihaning ma’lumotlar bazasi

---

## 🔐 Foydalanuvchi Funksiyalari

- Tizimda ro‘yxatdan o‘tish va login qilish
- Kurslarni ko‘rish va sotib olish
- Mentorlar ro‘yxati va profili
- Kursga yozilish va sharh qoldirish (review)
- Profil va buyurtmalarni boshqarish
- Parolni tiklash va o‘zgartirish
- To‘lov tizimi (Click, Payme va boshqalar uchun tayyor integratsiya)
- Admin panel orqali barcha ma’lumotlarni boshqarish

---

## 🖥️ Admin Panel

- Kurslar, mentorlar, studentlar, buyurtmalar, sharhlar va boshqalarni boshqarish
- Statistika va tezkor ko‘rsatkichlar
- Foydalanuvchilarni boshqarish

---

## 🎨 Dizayn

- Bootstrap asosida professional va responsive dizayn
- Qorong‘i (dark mode) va yorug‘ (light mode) rejim
- Zamonaviy UI komponentlar (modal, loader, alert, badge, avatar)
- Foydalanuvchi uchun qulay va tezkor interfeys

---

## 🧪 Test va Xatoliklarni Boshqarish

- Django test framework yordamida asosiy funksiyalar uchun testlar
- Har bir view va forma uchun xatoliklarni foydalanuvchiga ko‘rsatish
- Xavfsizlik: CSRF, XSS, va boshqa asosiy himoya choralari

---

## 🚀 Ishga Tushirish

```bash
git clone https://github.com/xalilov-max/Ake_fx.git
cd akefx
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # admin uchun
python manage.py runserver
```

## 📝 Hujjat va Qo‘llanma
-Kurs qo‘shish: Admin paneldan yangi kurs, mentor va darslarni qo‘shing.
-Foydalanuvchi ro‘yxatdan o‘tishi: /register/ sahifasi orqali.
-Sharh qoldirish: Kurs sotib olinganidan so‘ng, kursga sharh qoldirish -mumkin.
-To‘lov: Kurs sahifasida to‘lov tugmasi orqali.
-Profil: Foydalanuvchi o‘z profilini va buyurtmalarini boshqarishi -mumkin.

## 📞 Aloqa va Qo‘llab-quvvatlash
-Telegram: @akeFx_rasmiy
-Instagram: @ake__fx
-Email: info@akefx.com
