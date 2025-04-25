# app.py
#对比上一版本，增加auto_generate_template（），自动生成template
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_mysqldb import MySQL
import os
import re
from datetime import datetime
import pandas as pd
import datetime

app = Flask(__name__)
app.secret_key = 'gym_secret_2024'
app.config['MYSQL_HOST'] = '8.138.123.42'
app.config['MYSQL_PORT'] = 23036
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'gym_0424_generate_at_0424_2257'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Home page
@app.route('/', methods=['GET','POST'])
def index():
    role = session.get('role', 'guest')
    q = ''
    courses = []
    products = []
    if request.method == 'POST':
        q = request.form.get('q','').strip()
        if q:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Course WHERE name LIKE %s", (f'%{q}%',))
            courses = cur.fetchall()
            cur.execute("SELECT * FROM Product WHERE name LIKE %s", (f'%{q}%',))
            products = cur.fetchall()
    return render_template('index.html', role=role, courses=courses, products=products, q=q)

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("SELECT person_id, password, role, last_name FROM Person WHERE username=%s", (username,))
        u = cur.fetchone()
        if u and u['password'] == password and u['role'] == role:
            session['user_id'] = u['person_id']
            session['username'] = username
            session['role'] = role
            session['last_name'] = u['last_name']  # 这里加入存session
            flash("Login successful")
            return redirect(url_for('index'))
        else:
            flash("Login failed, please check username/password/permissions")
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET','POST'])
def register():
    cur = mysql.connection.cursor()
    cur.execute("SELECT branch_id, name, city, district FROM Branch")
    branches = cur.fetchall()
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        if not re.match(r'^1\d{10}$',request.form['phone']):
            flash('Incorrect format of mobile phone number ')
            return redirect(url_for('register'))#这里是检测号码是否符合标准
        id_number = request.form.get('id_number')
        password = request.form.get('password')
        branch_id = request.form.get('branch_id')
        specialty = request.form.get('specialty') if role=='coach' else None
        qualification_no = request.form.get('qualification_no') if role=='coach' else None
        qualification_expiry = request.form.get('qualification_expiry') if role=='coach' else None
        position = request.form.get('position') if role=='staff' else None
        join_date = datetime.now().date()
        # Uniqueness check
        cur.execute("SELECT person_id FROM Person WHERE username=%s", (username,))
        if cur.fetchone():
            flash("Username already exists")
            return render_template('register.html', branches=branches)
        try:
            cur.execute("""INSERT INTO Person(username, password, role, first_name, last_name,
            gender, birthday, phone, id_number, branch_id, join_date, specialty,
            qualification_no, qualification_expiry, position)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,(username,password,role,first_name,last_name,gender,birthday,phone,id_number,branch_id,join_date,
            specialty, qualification_no, qualification_expiry, position))
            mysql.connection.commit()
            flash("Registration successful, please log in")
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            print(e)
            flash("Registration exception")
            return render_template('register.html', branches=branches)
    return render_template('register.html', branches=branches)

# Course list
@app.route('/courses', methods=['GET','POST'])
def courses():
    q = ''
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        q = request.form.get('q','').strip()
        if q:
            cur.execute(
            "SELECT c.*,p.first_name,p.last_name FROM Course c"
            " LEFT JOIN Person p ON c.coach_id=p.person_id WHERE c.name LIKE %s", (f'%{q}%',))
            courses = cur.fetchall()
        else:
            cur.execute(
            "SELECT c.*,p.first_name,p.last_name FROM Course c"
            " LEFT JOIN Person p ON c.coach_id=p.person_id")
            courses = cur.fetchall()
    else:
        cur.execute(
        "SELECT c.*,p.first_name,p.last_name FROM Course c"
        " LEFT JOIN Person p ON c.coach_id=p.person_id")
        courses = cur.fetchall()
    # Count remaining seats
    for c in courses:
        cur.execute("SELECT COUNT(*) cnt FROM CourseEnrollment WHERE course_id=%s", (c['course_id'],))
        enrolled = cur.fetchone()['cnt']
        c['remain'] = c['max_seats'] - enrolled
        c['coach_name'] = (c['last_name'] or '') + (c['first_name'] or '')
    return render_template('courses.html', courses=courses, q=q)


# Course enrollment
@app.route('/enroll/<course_id>')
def enroll_course(course_id):
    if 'user_id' not in session or session.get('role')!='member':
        flash("Please log in as a member")
        return redirect(url_for('login'))
    uid = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CourseEnrollment WHERE course_id=%s AND member_id=%s", (course_id,uid))
    if cur.fetchone():
        flash("You have already registered for this course")
        return redirect(url_for('courses'))
    # Check remaining seats
    cur.execute("SELECT max_seats FROM Course WHERE course_id=%s", (course_id,))
    max_seats = cur.fetchone()['max_seats']
    cur.execute("SELECT COUNT(*) cnt FROM CourseEnrollment WHERE course_id=%s", (course_id,))
    enrolled = cur.fetchone()['cnt']
    if enrolled >= max_seats:
        flash("The course is full")
        return redirect(url_for('courses'))
    try:
        cur.execute("INSERT INTO CourseEnrollment(course_id,member_id) VALUES(%s,%s)", (course_id,uid))
        # Add consumption record
        cur.execute("SELECT fee FROM Course WHERE course_id=%s", (course_id,))
        fee = cur.fetchone()['fee']
        cur.execute("INSERT INTO Purchase(member_id,type,ref_id,number,total_fee) VALUES(%s,'course',%s,1,%s)", (uid,course_id,fee))
        mysql.connection.commit()
        flash("Registration successful, automatically charged")
    except Exception as e:
        print(e)
        mysql.connection.rollback()
        flash("Registration failed")
    return redirect(url_for('courses'))

#报名课程实例/新增,对于一个课程的！！
@app.route('/enroll_instance/<course_instance_id>')
def enroll_instance(course_instance_id):
    if 'user_id' not in session or session.get('role') != 'member':
        flash("Please log in as a member")
        return redirect(url_for('login'))

    uid = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CourseEnrollment WHERE course_id=%s AND member_id=%s", (course_instance_id, uid))
    if cur.fetchone():
        flash("You have already enrolled in this course")
        return redirect(url_for('course_instances'))

    # 改为从 Course 表获取 max_seats 和 fee
    cur.execute("""
        SELECT c.max_seats, c.fee
        FROM CourseInstance ci
        JOIN Course c ON ci.course_id = c.course_id
        WHERE ci.course_instance_id=%s
    """, (course_instance_id,))
    data = cur.fetchone()

    cur.execute("SELECT COUNT(*) cnt FROM CourseEnrollment WHERE course_id=%s", (course_instance_id,))
    enrolled = cur.fetchone()['cnt']
    if enrolled >= data['max_seats']:
        flash("The course is full")
        return redirect(url_for('course_instances'))

    try:
        cur.execute("INSERT INTO CourseEnrollment(course_id, member_id) VALUES(%s, %s)", (course_instance_id, uid))
        cur.execute("INSERT INTO Purchase(member_id, type, ref_id, number, total_fee) VALUES(%s, 'course', %s, 1, %s)", (uid, course_instance_id, data['fee']))
        mysql.connection.commit()
        flash("Successfully enrolled, fee charged")
    except Exception as e:
        print(e)
        mysql.connection.rollback()
        flash("Enrollment failed")
    return redirect(url_for('course_instances'))

# Course withdrawal
@app.route('/quit/<course_id>')
def quit_course(course_id):
    if 'user_id' not in session or session.get('role')!='member':
        return redirect(url_for('login'))
    uid = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM CourseEnrollment WHERE course_id=%s AND member_id=%s", (course_id,uid))
    cur.execute("DELETE FROM Purchase WHERE type='course' AND ref_id=%s AND member_id=%s", (course_id,uid))
    mysql.connection.commit()
    flash("Course withdrawn")
    return redirect(url_for('my_purchase'))

#新增，课程模板管理
@app.route('/course_template_manage')
def course_template_manage():
    if session.get('role') != 'admin':
        flash("仅管理员可访问")
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CourseTemplate")
    templates = cur.fetchall()

    return render_template("course_template_manage.html", templates=templates)
    
#新增路由
@app.route('/add_course_template', methods=['POST'])
def add_course_template():
    form = request.form

    name = form['name']
    coach_id = form['coach_id']
    branch_id = form['branch_id']
    location = form['location']
    weekly = int(form['weekly'])
    requirement = form.get('requirement', '')

    # 引用课程
    course_id = form['course_id']
    course_name = form['course_name']

    # 从 Course 表中获取课程时间、有效期、费用、座位等
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT start_date, end_date, start_time, end_time, max_seats, fee
        FROM Course WHERE course_id = %s
    """, (course_id,))
    course_info = cur.fetchone()

    if not course_info:
        flash("Course not found.")
        return redirect(url_for('course_template_manage'))

    # 自动同步字段
    valid_from = course_info['start_date']
    valid_to = course_info['end_date']
    start_time = course_info['start_time']
    end_time = course_info['end_time']
    max_seats = course_info['max_seats']
    fee = course_info['fee']

    # 插入模板
    cur.execute("""
        INSERT INTO CourseTemplate (
            name, coach_id, branch_id, location, weekly, start_time, end_time,
            valid_from, valid_to, max_seats, fee, requirement, course_id, course_name
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, coach_id, branch_id, location, weekly, start_time, end_time,
          valid_from, valid_to, max_seats, fee, requirement, course_id, course_name))
    mysql.connection.commit()

    template_id = cur.lastrowid

    # 生成周期课程实例
    generate_course_instances(
        cur, template_id, course_id, course_name, weekly,
        start_time, end_time, valid_from, valid_to
    )

    flash("Template created and instances generated successfully.")
    return redirect(url_for('course_template_manage'))


#课程实例
@app.route('/course_instances')
def course_instances():
    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT ci.*, ct.location, ct.fee, ct.max_seats, p.first_name, p.last_name
    FROM CourseInstance ci
    JOIN CourseTemplate ct ON ci.template_id = ct.template_id
    JOIN Person p ON ct.coach_id = p.person_id
    WHERE ci.member_id = %s
    ORDER BY ci.start_datetime
""", (session['user_id'],))
    instances = cur.fetchall()

    for c in instances:
        cur.execute("SELECT COUNT(*) cnt FROM CourseEnrollment WHERE course_id=%s", (c['course_instance_id'],))
        enrolled = cur.fetchone()['cnt']
        c['remain'] = c['max_seats'] - enrolled
        c['coach_name'] = (c['last_name'] or '') + (c['first_name'] or '')

    return render_template('course_instances.html', instances=instances)

@app.route('/auto_generate_template/<course_id>')
def auto_generate_template(course_id):
    if 'user_id' not in session or session.get('role') != 'member':
        flash("Please login as member.")
        return redirect(url_for('login'))
    member_id = session['user_id']
    cur = mysql.connection.cursor()

    # 查询课程信息
    cur.execute("SELECT * FROM Course WHERE course_id = %s", (course_id,))
    c = cur.fetchone()
    if not c:
        flash("Course not found.")
        return redirect(url_for('courses'))

    # 用 datetime 解析 weekday
    weekly = datetime.strptime(str(c['start_date']), "%Y-%m-%d").weekday()

    # 时间字段修正（确保为 datetime.time）
    if isinstance(c['start_time'], str):
        c['start_time'] = datetime.strptime(c['start_time'], "%H:%M:%S").time()
    if isinstance(c['end_time'], str):
        c['end_time'] = datetime.strptime(c['end_time'], "%H:%M:%S").time()

    # 插入模板
    cur.execute("""
        INSERT INTO CourseTemplate (
            name, coach_id, branch_id, location, weekly,
            start_time, end_time, valid_from, valid_to,
            max_seats, fee, requirement, course_id, course_name
        ) VALUES (%s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        c['name'], c['coach_id'], c['branch_id'], c['location'], weekly,
        c['start_time'], c['end_time'], c['start_date'], c['end_date'],
        c['max_seats'], c['fee'], c['requirement'], c['course_id'], c['name']
    ))
    mysql.connection.commit()
    template_id = cur.lastrowid

    # 生成实例
    generate_course_instances(cur, template_id, course_id, c['name'], weekly,
                              c['start_time'], c['end_time'], c['start_date'], c['end_date'], member_id)

    flash("Cycle template & instances generated.")
    return redirect(url_for('course_instances'))


# Product list
@app.route('/products', methods=['GET','POST'])
def products():
    q = ''
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        q = request.form.get('q','').strip()
        if q:
            cur.execute("SELECT * FROM Product WHERE name LIKE %s", (f'%{q}%',))
            products = cur.fetchall()
        else:
            cur.execute("SELECT * FROM Product")
            products = cur.fetchall()
    else:
        cur.execute("SELECT * FROM Product")
        products = cur.fetchall()
    return render_template('products.html', products=products, q=q)

# Product purchase
@app.route('/buy/<product_id>')
def buy_product(product_id):
    if 'user_id' not in session or session.get('role')!='member':
        flash("Please log in as a member to purchase")
        return redirect(url_for('login'))
    uid = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT stock FROM Product WHERE product_id=%s", (product_id,))
    row = cur.fetchone()
    if not row or row['stock']<=0:
        flash('Sold out')
        return redirect(url_for('products'))
    # Deduct stock
    cur.execute("UPDATE Product SET stock=stock-1 WHERE product_id=%s AND stock>0", (product_id,))
    cur.execute("SELECT name FROM Product WHERE product_id=%s", (product_id,))
    cur.execute("INSERT INTO Purchase(member_id,type,ref_id,number,total_fee) VALUES(%s,'product',%s,1,10.0)", (uid,product_id)) # Assume price is 10
    mysql.connection.commit()
    flash("Purchase successful!")
    return redirect(url_for('products'))

# My purchases
@app.route('/my_purchase', methods=['GET','POST'])
def my_purchase():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    uid = session['user_id']
    cur = mysql.connection.cursor()
    q = ''
    if request.method=='POST':
        q = request.form.get('q','').strip()
    sql = """
    SELECT p.purchase_id,p.type,p.ref_id,
        CASE
            WHEN p.type='course' THEN (SELECT name FROM Course WHERE course_id=p.ref_id)
            ELSE (SELECT name FROM Product WHERE product_id=p.ref_id)
        END AS item_name,
        p.number, p.total_fee, p.purchase_time
    FROM Purchase p
    WHERE p.member_id=%s
    """
    args = [uid]
    if q:
        sql += " AND (p.ref_id LIKE %s OR EXISTS(SELECT 1 FROM Course WHERE course_id=p.ref_id AND name LIKE %s) OR EXISTS(SELECT 1 FROM Product WHERE product_id=p.ref_id AND name LIKE %s))"
        kw = f'%{q}%'
        args += [kw,kw,kw]
    sql += " ORDER BY p.purchase_time DESC"
    cur.execute(sql, tuple(args))
    records = cur.fetchall()
    return render_template('my_purchase.html', records=records, q=q)

# Coach schedule
@app.route('/coach_schedule')
def coach_schedule():
    if session.get('role') != 'coach':
        flash("Please log in as a coach")
        return redirect(url_for('login'))
    uid = session['user_id']
    cur = mysql.connection.cursor()

    # 查该教练名下课程
    cur.execute("""
        SELECT * FROM Course WHERE coach_id = %s
    """, (uid,))
    courses = cur.fetchall()

    schedule = []
    for course in courses:
        course_id = course['course_id']

        # 查该课程名下所有课程实例
        cur.execute("""
            SELECT ci.*, ct.location
            FROM CourseInstance ci
            JOIN CourseTemplate ct ON ci.template_id = ct.template_id
            WHERE ci.course_id = %s
            ORDER BY ci.start_datetime
        """, (course_id,))
        instances = cur.fetchall()

        for ci in instances:
            # 查该节课所有报名学员
            cur.execute("""
                SELECT p.first_name, p.last_name, p.gender, p.phone
                FROM CourseEnrollment ce
                JOIN Person p ON ce.member_id = p.person_id
                WHERE ce.course_id = %s
            """, (ci['course_instance_id'],))
            ci['students'] = cur.fetchall()
        
        schedule.append({
            'course': course,
            'instances': instances
        })
    
    return render_template('coach_schedule.html', schedule=schedule)




@app.route('/branch_manage')
def branch_manage():
    # 仅管理员可访问
    if session.get('role') != 'admin':
        flash("仅限管理员访问")
        return redirect(url_for('index'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Branch")
    branches = cur.fetchall()
    return render_template('branch_manage.html', branches=branches)

@app.route('/add_branch', methods=['POST'])
def add_branch():
    if session.get('role') != 'admin':
        flash("非法操作")
        return redirect(url_for('index'))
    name = request.form['name']
    city = request.form['city']
    district = request.form['district']
    address = request.form['address']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Branch(name, city, district, address) VALUES(%s, %s, %s, %s)",
                (name, city, district, address))
    mysql.connection.commit()
    flash("分店添加成功")
    return redirect(url_for('branch_manage'))

@app.route('/edit_branch/<int:branch_id>', methods=['POST'])
def edit_branch(branch_id):
    if session.get('role') != 'admin':
        flash("非法操作")
        return redirect(url_for('index'))
    name = request.form['name']
    city = request.form['city']
    district = request.form['district']
    address = request.form['address']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Branch SET name=%s, city=%s, district=%s, address=%s WHERE branch_id=%s",
                (name, city, district, address, branch_id))
    mysql.connection.commit()
    flash("分店修改成功")
    return redirect(url_for('branch_manage'))

@app.route('/delete_branch/<int:branch_id>')
def delete_branch(branch_id):
    if session.get('role') != 'admin':
        flash("非法操作")
        return redirect(url_for('index'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Branch WHERE branch_id=%s", (branch_id,))
    mysql.connection.commit()
    flash("分店删除成功")
    return redirect(url_for('branch_manage'))

@app.route('/admin_manage')
def admin_manage():
    """
    Admin staff and member management interface. Lists and allows editing/deleting users.
    """
    # Restrict page to admin role only
    if session.get('role') != 'admin':
        flash("Unauthorized access.")
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()

    # Query staff and admin users
    cur.execute("""
        SELECT p.person_id, p.username, p.first_name, p.last_name, p.role, p.phone, b.name AS branch_name
        FROM Person p
        LEFT JOIN Branch b ON p.branch_id = b.branch_id
        WHERE p.role IN ('staff', 'admin')
    """)
    staff_list = cur.fetchall()

    # Query member users
    cur.execute("""
        SELECT p.person_id, p.username, p.first_name, p.last_name, p.role, p.phone, b.name AS branch_name
        FROM Person p
        LEFT JOIN Branch b ON p.branch_id = b.branch_id
        WHERE p.role = 'member'
    """)
    member_list = cur.fetchall()

    return render_template('admin_manage.html', staff_list=staff_list, member_list=member_list)

@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    if session.get('role') != 'admin':
        flash("非法操作")
        return redirect(url_for('index'))
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    role = request.form.get('role')
    cur = mysql.connection.cursor()
    cur.execute("""
    UPDATE Person SET first_name=%s, last_name=%s, phone=%s, role=%s WHERE person_id=%s
    """, (first_name, last_name, phone, role, user_id))
    mysql.connection.commit()
    flash("用户信息更新成功")
    return redirect(url_for('admin_manage'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if session.get('role') != 'admin':
        flash("Illegal operation")
        return redirect(url_for('index'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Person WHERE person_id=%s", (user_id,))
    mysql.connection.commit()
    flash("The user information was deleted successfully")
    return redirect(url_for('admin_manage'))

@app.route('/equipment_manage')
def equipment_manage():
    role = session.get('role')
    if role not in ['admin', 'staff']:
        flash("Permission denied.")
        return redirect(url_for('index'))

    # 获取排序和筛选参数，默认按ID排序
    sort = request.args.get('sort', 'equipment_id')
    status_filter = request.args.get('status', '')  # 获取筛选状态

    # 构建基本SQL
    sql = """
        SELECT e.equipment_id, e.name, e.quantity, e.status, e.branch_id, b.name as branch_name
        FROM Equipment e
        JOIN Branch b ON e.branch_id = b.branch_id
    """

    params = []

    # 加入筛选条件
    if status_filter:
        sql += " WHERE e.status = %s"
        params.append(status_filter)

    # 加入排序条件
    allowed_sort_columns = {
        'equipment_id': 'e.equipment_id',
        'name': 'e.name',
        'quantity': 'e.quantity',
        'status': 'e.status',
        'branch_name': 'b.name'
    }
    order_column = allowed_sort_columns.get(sort, 'e.equipment_id')
    sql += f" ORDER BY {order_column}"

    cur = mysql.connection.cursor()
    cur.execute(sql, tuple(params))
    equipment_list = cur.fetchall()

    # 查询所有分店，提供筛选条件（如果页面需要）
    cur.execute("SELECT branch_id, name FROM Branch")
    branches = cur.fetchall()

    return render_template('equipment_manage.html', equipment_list=equipment_list, branches=branches)

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    """
    Add new equipment to the database. Accessible by admin and staff.
    """
    role = session.get('role')
    if role not in ['admin', 'staff']:
        flash("You are not authorized to perform this action.")
        return redirect(url_for('index'))

    # Get form data
    name = request.form['name']
    quantity = request.form['quantity']
    status = request.form['status']
    branch_id = request.form['branch_id']

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO Equipment (name, quantity, status, branch_id)
            VALUES (%s, %s, %s, %s)
        """, (name, quantity, status, branch_id))
        mysql.connection.commit()
        flash("Equipment added successfully!")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error adding equipment: {str(e)}")

    return redirect(url_for('equipment_manage'))


@app.route('/delete_equipment/<int:equipment_id>', methods=['GET'])
def delete_equipment(equipment_id):
    """
    Delete equipment record from the database. Accessible by admin and staff.
    """
    role = session.get('role')
    if role not in ['admin', 'staff']:
        flash("You are not authorized to perform this action.")
        return redirect(url_for('index'))

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Equipment WHERE equipment_id = %s", (equipment_id,))
        mysql.connection.commit()
        flash("Equipment deleted successfully!")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error deleting equipment: {str(e)}")

    return redirect(url_for('equipment_manage'))



@app.route('/lost_and_found')
def lost_and_found():
    page = request.args.get('page', default=1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    cur = mysql.connection.cursor()
    
    # 获取总数（用于分页）
    cur.execute("SELECT COUNT(*) AS total FROM LostAndFound")
    total = cur.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page  # 向上取整

    # 分页查询当前页数据
    cur.execute("""
    SELECT * FROM lostandfound
    ORDER BY pick_time DESC
    LIMIT %s OFFSET %s
""", (per_page, offset))
    items = cur.fetchall()

    return render_template('lost_and_found.html', items=items, page=page, total_pages=total_pages)



@app.route('/add_lost_item', methods=['POST'])
def add_lost_item():
    if 'username' not in session:
        flash("Please log in to add a lost item.")
        return redirect(url_for('login'))

    pick_name = request.form['pick_name']
    pick_time_str = request.form.get('pick_time')
    pick_time = datetime.strptime(pick_time_str, '%Y-%m-%dT%H:%M') if pick_time_str else datetime.now()
    pick_place = request.form['pick_place']
    description = request.form['description']
    registrant_username = session['username']

    photo = request.files.get('pick_photo')
    pick_photo = None

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO LostAndFound (pick_name, pick_time, pick_place, description, registrant_username)
            VALUES (%s, %s, %s, %s, %s)
        """, (pick_name, pick_time, pick_place, description or None, registrant_username))
        mysql.connection.commit()

        pick_id = cur.lastrowid

        if photo:
            # 修改文件名格式
            photo_filename = f"pick_{pick_id}_{pick_name}.jpg"
            photo_path = os.path.join('static/images', photo_filename)
            photo.save(photo_path)
            cur.execute("UPDATE LostAndFound SET pick_photo = %s WHERE pick_id = %s", (photo_filename, pick_id))
            mysql.connection.commit()

        flash("Lost item added successfully!")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error adding lost item: {str(e)}")

    return redirect(url_for('lost_and_found'))


@app.route('/claim_lost_item/<int:pick_id>')
def claim_lost_item(pick_id):
    if 'username' not in session:
        flash("Please log in to claim a lost item.")
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE LostAndFound SET is_claimed = TRUE WHERE pick_id = %s", (pick_id,))
        mysql.connection.commit()
        flash("Item claimed successfully!")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error claiming item: {str(e)}")

    return redirect(url_for('lost_and_found'))


# Data dashboard
@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'admin':
        flash("Admin access only")
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(DISTINCT member_id) as cnt FROM Purchase WHERE DATE(purchase_time)=CURDATE()")
    today_visit = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM Person WHERE role='member'")
    total_member = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM Person WHERE role='coach'")
    total_coach = cur.fetchone()['cnt']
    # Age groups
    cur.execute("""SELECT
    CASE 
      WHEN TIMESTAMPDIFF(YEAR,birthday,CURDATE())<18 THEN 'Under 18'
      WHEN TIMESTAMPDIFF(YEAR,birthday,CURDATE())<25 THEN '18-24'
      WHEN TIMESTAMPDIFF(YEAR,birthday,CURDATE())<35 THEN '25-34'
      WHEN TIMESTAMPDIFF(YEAR,birthday,CURDATE())<45 THEN '35-44'
      ELSE '45 and above'
    END AS age_group, COUNT(*) as cnt
    FROM Person WHERE role='member' GROUP BY age_group""")
    age_groups = {r['age_group']:r['cnt'] for r in cur.fetchall()}
    cur.execute("SELECT gender,COUNT(*) as cnt FROM Person WHERE role='member' GROUP BY gender")
    gender_groups = {'Male':0,'Female':0}
    for r in cur.fetchall():
        if r['gender']=='M': gender_groups['Male']+=r['cnt']
        elif r['gender']=='F': gender_groups['Female']+=r['cnt']
        else: gender_groups.setdefault('Other',0)
    stat = dict(today_visit=today_visit, total_member=total_member, total_coach=total_coach,
       age_groups=age_groups, gender_groups=gender_groups)
    return render_template('dashboard.html', stat=stat)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#工具函数
from datetime import datetime, timedelta, time

def generate_course_instances(cur, template_id, course_id, course_name, weekly, start_time, end_time, valid_from, valid_to,member_id):
    if isinstance(start_time, timedelta):
        start_time = (datetime.min + start_time).time()
    elif isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%H:%M:%S").time()

    if isinstance(end_time, timedelta):
        end_time = (datetime.min + end_time).time()
    elif isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%H:%M:%S").time()
    # 开始生成课程实例
    date = valid_from
    while date <= valid_to:
        if date.weekday() == weekly:
            start_dt = datetime.combine(date, start_time)
            end_dt = datetime.combine(date, end_time)
            course_instance_id = f"{course_id}_{date.strftime('%Y%m%d')}"
            cur.execute("""
        INSERT INTO CourseInstance (
            course_instance_id, course_name, template_id, course_id,
            start_datetime, end_datetime, status, member_id
        ) VALUES (%s, %s, %s, %s, %s, %s, 'present', %s)
    """, (course_instance_id, course_name, template_id, course_id, start_dt, end_dt, member_id))
        date += timedelta(days=1)
    mysql.connection.commit()

@app.route('/user_profile')
def user_profile():
    if 'user_id' not in session:
        flash("请先登录")
        return redirect(url_for('login'))
    
    uid = session['user_id']
    cur = mysql.connection.cursor()
    
    # 获取用户基本信息
    cur.execute("""
        SELECT p.*, b.name as branch_name
        FROM Person p
        LEFT JOIN Branch b ON p.branch_id = b.branch_id
        WHERE p.person_id = %s
    """, (uid,))
    user_info = cur.fetchone()
    
    # 获取用户的课程信息
    cur.execute("""
        SELECT c.name, c.start_date, c.end_date, c.start_time, c.end_time, c.location
        FROM CourseEnrollment ce
        JOIN Course c ON ce.course_id = c.course_id
        WHERE ce.member_id = %s
    """, (uid,))
    enrolled_courses = cur.fetchall()
    
    # 获取用户的购买记录
    cur.execute("""
        SELECT p.type, p.ref_id, p.number, p.total_fee, p.purchase_time,
               CASE
                   WHEN p.type='course' THEN (SELECT name FROM Course WHERE course_id=p.ref_id)
                   ELSE (SELECT name FROM Product WHERE product_id=p.ref_id)
               END AS item_name
        FROM Purchase p
        WHERE p.member_id = %s
        ORDER BY p.purchase_time DESC
        LIMIT 5
    """, (uid,))
    recent_purchases = cur.fetchall()
    
    return render_template('user_profile.html', 
                         user_info=user_info,
                         enrolled_courses=enrolled_courses,
                         recent_purchases=recent_purchases)

if __name__=="__main__":
    if not os.path.isdir('static/images'):
        os.makedirs('static/images')
    app.run(debug=True)


