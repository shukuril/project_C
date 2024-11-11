// Массив с данными меню
const menuItems = [
    {
        name: 'Салат Цезарь',
        category: 'starters',
        price: '300 ₽',
        image: 'img1.jpeg',
        description: 'Классический салат с курицей, листьями салата и сыром пармезан.',
    },
    {
        name: 'Стейк из говядины',
        category: 'mains',
        price: '1200 ₽',
        image: 'img.jpeg',
        description: 'Сочный стейк с гарниром из овощей.',
    },
    {
        name: 'Шоколадный фондан',
        category: 'desserts',
        price: '450 ₽',
        image: 'img2.jpeg',
        description: 'Теплый шоколадный десерт с жидкой начинкой.',
    },
    {
        name: 'Лимонад',
        category: 'drinks',
        price: '200 ₽',
        image: 'img3.jpeg',
        description: 'Освежающий домашний лимонад.',
    }
];

// Функция для отображения всех элементов меню
function displayMenu(items) {
    const menuContainer = document.getElementById('menu');
    menuContainer.innerHTML = '';  // Очищаем контейнер

    items.forEach(item => {
        const menuItem = document.createElement('div');
        menuItem.classList.add('menu-item');
        menuItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <h3>${item.name}</h3>
            <p class="description">${item.description}</p>
            <p class="price">${item.price}</p>
        `;
        menuContainer.appendChild(menuItem);
    });
}

// Функция для фильтрации элементов меню по категории
function filterMenu(category) {
    if (category === 'all') {
        displayMenu(menuItems);
    } else {
        const filteredItems = menuItems.filter(item => item.category === category);
        displayMenu(filteredItems);
    }
}

// Функция для открытия и закрытия скрывающегося меню
function toggleMenu() {
    const navbar = document.getElementById("navbar");
    navbar.classList.toggle("show");
}

// Изначально отображаем все элементы
displayMenu(menuItems);

// Кнопка "Наверх"
window.onscroll = function () {
    const backToTopButton = document.getElementById("backToTop");
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
};

// Прокрутка наверх
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}
