from flask import Flask, render_template, jsonify  # 正确的：Flask 大写
app = Flask(__name__)

# 商品数据
products = [
    {"id": 1, "name": "冰箱", "category": "家电", "price": 2999, "free_shipping": True},
    {"id": 2, "name": "耳机", "category": "家电", "price": 199, "free_shipping": True},
    {"id": 3, "name": "T恤", "category": "服装", "price": 99, "free_shipping": False},
    {"id": 4, "name": "饼干", "category": "食品", "price": 29, "free_shipping": True},
    {"id": 5, "name": "洗衣机", "category": "家电", "price": 1599, "free_shipping": True},
    {"id": 6, "name": "牛仔裤", "category": "服装", "price": 299, "free_shipping": False},
    {"id": 7, "name": "巧克力", "category": "食品", "price": 59, "free_shipping": True},
    {"id": 8, "name": "笔记本电脑", "category": "家电", "price": 5999, "free_shipping": True},
    {"id": 9, "name": "运动鞋", "category": "服装", "price": 699, "free_shipping": False},
    {"id": 10, "name": "面包", "category": "食品", "price": 15, "free_shipping": False}
]

# 辅助函数：将商品列表转换为集合（使用id作为标识）
def to_set(product_list):
    return set(product["id"] for product in product_list)

# 辅助函数：根据id集合获取商品列表
def get_products_by_ids(id_set):
    return [p for p in products if p["id"] in id_set]

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/filter-page')
def index():
    return render_template('index.html', products=products)

@app.route('/filter', methods=['GET'])
def filter_products():
    from flask import request
    
    # 获取筛选条件
    categories = request.args.getlist('category')
    price_range = request.args.get('price_range', '')
    free_shipping = request.args.get('free_shipping', '')
    
    # 全集合
    all_products = to_set(products)
    result_set = all_products.copy()
    expression_parts = []
    
    # 处理类别筛选（多选项，"或"关系，对应并集）
    if categories:
        category_sets = []
        for cat in categories:
            cat_set = to_set([p for p in products if p["category"] == cat])
            category_sets.append(cat_set)
        
        # 计算并集
        category_result = set().union(*category_sets)
        result_set &= category_result
        
        # 构建表达式
        cat_expr = " ∪ ".join([f"{cat}集合" for cat in categories])
        if len(categories) > 1:
            cat_expr = f"({cat_expr})"
        expression_parts.append(cat_expr)
    
    # 处理价格区间筛选
    if price_range:
        price_set = set()
        expr = ""
        
        if price_range == "0-100":
            price_set = to_set([p for p in products if 0 <= p["price"] <= 100])
            expr = "0-100元集合"
        elif price_range == "100-500":
            price_set = to_set([p for p in products if 100 < p["price"] <= 500])
            expr = "100-500元集合"
        elif price_range == "500+":
            price_set = to_set([p for p in products if p["price"] > 500])
            expr = "500元以上集合"
        
        result_set &= price_set
        expression_parts.append(expr)
    
    # 处理包邮筛选
    if free_shipping:
        shipping_set = set()
        expr = ""
        
        if free_shipping == "yes":
            shipping_set = to_set([p for p in products if p["free_shipping"]])
            expr = "包邮集合"
        elif free_shipping == "no":
            # 补集：不包邮是包邮集合的补集
            shipping_set = all_products - to_set([p for p in products if p["free_shipping"]])
            expr = "非包邮集合"
        
        result_set &= shipping_set
        expression_parts.append(expr)
    
    # 构建集合运算表达式
    if expression_parts:
        expression = " ∩ ".join(expression_parts)
    else:
        expression = "全集合"
    
    # 获取符合条件的商品
    filtered_products = get_products_by_ids(result_set)
    
    return jsonify(
        {
        "products": filtered_products,
        "expression": expression
    }
    )

if __name__ == '__main__':
    app.run(debug=False, port=5001)  # 改为 debug=False