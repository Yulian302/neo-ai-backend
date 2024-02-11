const currentPath = window.location.pathname
let page = currentPath.split('/')
page = page[page.length - 2]
const settingsList = ['general', 'security', 'notifications']
if (settingsList.includes(page)) {
  const activeSection = document.getElementById(page)
  activeSection.classList.add('activeSection')
  activeSection.classList.remove('hover:bg-gray-100')
}

