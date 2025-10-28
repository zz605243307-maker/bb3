document.addEventListener('DOMContentLoaded', function() {
    // 获取所有筛选控件
    const categoryCheckboxes = document.querySelectorAll('input[name="category"]');
    const priceRangeSelect = document.getElementById('priceRange');
    const shippingRadios = document.querySelectorAll('input[name="free_shipping"]');
    
    // 当筛选条件变化时触发筛选
    function handleFilterChange() {
        // 收集筛选条件
        const categories = Array.from(categoryCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
        
        const priceRange = priceRangeSelect.value;
        
        const freeShipping = Array.from(shippingRadios)
            .find(radio => radio.checked)
            .value;
        
        // 构建查询字符串
        const params = new URLSearchParams();
        categories.forEach(cat => params.append('category', cat));
        if (priceRange) params.append('price_range', priceRange);
        if (freeShipping) params.append('free_shipping', freeShipping);
        
        // 发送请求
        fetch(`/filter?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                // 更新表达式
                document.getElementById('expression').textContent = data.expression;
                
                // 更新筛选结果
                const resultsContainer = document.getElementById('filteredProducts');
                resultsContainer.innerHTML = '';
                
                if (data.products.length === 0) {
                    resultsContainer.innerHTML = '<div class="col-12"><p class="text-center">没有找到符合条件的商品</p></div>';
                    return;
                }
                
                data.products.forEach(product => {
                    const productCard = `
                        <div class="col-md-3 mb-3">
                            <div class="card product-card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">${product.name}</h5>
                                    <p class="card-text">
                                        类别: ${product.category}<br>
                                        价格: ${product.price}元<br>
                                        包邮: ${product.free_shipping ? '是' : '否'}
                                    </p>
                                </div>
                            </div>
                        </div>
                    `;
                    resultsContainer.innerHTML += productCard;
                });
            })
            .catch(error => console.error('筛选出错:', error));
    }
    
    // 为所有筛选控件添加事件监听器
    categoryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleFilterChange);
    });
    
    priceRangeSelect.addEventListener('change', handleFilterChange);
    
    shippingRadios.forEach(radio => {
        radio.addEventListener('change', handleFilterChange);
    });
});