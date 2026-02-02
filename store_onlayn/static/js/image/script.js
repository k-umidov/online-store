setTimeout(function(){
    document.getElementById('message').style.display = 'none';
}, 3000);

const orderBtn = document.querySelector('.my_orders')
    const listOrders = document.querySelector('.list_orders')
    const arrowDown = document.querySelector('.errow_down')
    orderBtn.addEventListener('click', () => {
      listOrders.classList.toggle('active')
      arrowDown.classList.toggle('active')
    });


const orderBtn2 = document.querySelector('.answer-review')
    let listOrders2 = document.querySelector('.answer-form')

    orderBtn2.addEventListener('click', () => {
      listOrders2.classList.toggle('active_review')

    });

document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.filter-btn');

  buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation(); // чтобы клик не дошел до document
      const dropdown = btn.dataset.dropdown;
      const menu = document.querySelector(`.filter-menu[data-dropdown-menu="${dropdown}"]`);

      document.querySelectorAll('.filter-menu').forEach(m => {
        if (m !== menu) m.style.display = 'none';
      });

      menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
    });
  });

  document.addEventListener('click', () => {
    document.querySelectorAll('.filter-menu').forEach(m => m.style.display = 'none');
  });
});
document.addEventListener('DOMContentLoaded', function() {
  const filterDropdowns = document.querySelectorAll('.filter-dropdown');
  const overlay = document.querySelector('.filter-overlay');

  filterDropdowns.forEach(dropdown => {
    const btn = dropdown.querySelector('.filter-btn');

    btn.addEventListener('click', function() {
      // Закрываем все другие открытые dropdown
      filterDropdowns.forEach(d => {
        if (d !== dropdown) d.classList.remove('active');
      });

      // Переключаем текущий dropdown
      dropdown.classList.toggle('active');

      // Переключаем overlay
      const anyActive = document.querySelector('.filter-dropdown.active');
      overlay.classList.toggle('active', !!anyActive);
    });
  });

  // Закрытие при клике на overlay
  overlay.addEventListener('click', function() {
    filterDropdowns.forEach(d => d.classList.remove('active'));
    overlay.classList.remove('active');
  });
});
