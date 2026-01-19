from flask import Blueprint, render_template, request, redirect, url_for, flash
from Forms import FAQForm
import sqlite3

faq_blueprint = Blueprint('faq', __name__)

# Connect helper
def get_db_connection():
    conn = sqlite3.connect('whatsup.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@faq_blueprint.route('/')
def home():
    return render_template("home.html")

# List FAQs
@faq_blueprint.route('/faq/list')
def list_faqs():
    conn = get_db_connection()
    faqs = conn.execute("SELECT * FROM faqs").fetchall()
    conn.close()
    return render_template("faqList.html", faqs=faqs)

# Create FAQ
@faq_blueprint.route('/faq/create', methods=['GET', 'POST'])
def create_faq():
    form = FAQForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = form.question.data
        answer = form.answer.data
        category = form.category.data
        tags = form.tags.data
        status = form.status.data

        conn = get_db_connection()
        conn.execute("INSERT INTO faqs (question, answer, category, tags, status) VALUES (?, ?, ?, ?, ?)",
                     (question, answer, category, tags, status))
        conn.commit()
        conn.close()

        flash("✅ FAQ created successfully!", "success")
        return redirect(url_for('faq.list_faqs'))

    return render_template("createFAQ.html", form=form)

# Edit FAQ
@faq_blueprint.route('/faq/edit/<int:id>', methods=['GET', 'POST'])
def edit_faq(id):
    conn = get_db_connection()
    faq = conn.execute("SELECT * FROM faqs WHERE id = ?", (id,)).fetchone()

    if faq is None:
        flash("❌ FAQ not found.", "danger")
        return redirect(url_for('faq.list_faqs'))

    form = FAQForm(data=faq)

    if request.method == 'POST' and form.validate_on_submit():
        conn.execute("UPDATE faqs SET question = ?, answer = ?, category = ?, tags = ?, status = ? WHERE id = ?",
                     (form.question.data, form.answer.data, form.category.data, form.tags.data, form.status.data, id))
        conn.commit()
        conn.close()

        flash("✅ FAQ updated successfully!", "success")
        return redirect(url_for('faq.list_faqs'))

    conn.close()
    return render_template("editFAQ.html", form=form, faq=faq)

# Delete FAQ
@faq_blueprint.route('/faq/delete/<int:id>', methods=['POST'])
def delete_faq(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM faqs WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("🗑️ FAQ deleted.", "info")
    return redirect(url_for('faq.list_faqs'))

# ✅ Analytics Page
@faq_blueprint.route('/faq/analytics')
def faq_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM faqs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM faqs WHERE status = 'published'")
    published = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM faqs WHERE status = 'draft'")
    draft = cursor.fetchone()[0]

    conn.close()

    return render_template("faqAnalytics.html", total=total, published=published, draft=draft)
