const currentPage = window.location.pathname
let pageName = currentPage.slice(1, -1)
const activePages = ['dashboard', 'team', 'models']
let isSettings = pageName.split('/')[0] === 'settings'
if (activePages.includes(pageName) || isSettings) {
  if (window.innerWidth <= 640) {
    pageName += 'mob'
  }
  let activeNavButton = null
  if (isSettings) {
    activeNavButton = document.getElementById('settings')
  } else {
    activeNavButton = document.getElementById(pageName)
  }
  activeNavButton.classList.add('activeButton')
  activeNavButton.classList.remove('hover:bg-gray-700')
}

function toggleMobileMenu () {
  const menu = document.getElementById('mobile-menu')
  if (menu.classList.contains('hidden')) {
    menu.classList.remove('hidden')
  } else {
    menu.classList.add('hidden')
  }
}
