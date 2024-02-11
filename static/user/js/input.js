function toggleInput (fieldName) {
  const displayElement = document.getElementById(`${fieldName}Display`)
  const inputElement = document.getElementById(`${fieldName}Input`)
  const updateButton = document.getElementById(`${fieldName}Update`)
  const saveButton = document.getElementById(`${fieldName}Save`)

  if (displayElement && inputElement) {
    const isInputHidden = inputElement.classList.contains('hidden')
    if (isInputHidden) {
      displayElement.classList.add('hidden')
      inputElement.classList.remove('hidden')
      updateButton.classList.add('hidden')
      saveButton.classList.remove('hidden')
    } else {
      displayElement.classList.remove('hidden')
      inputElement.classList.add('hidden')
      updateButton.classList.remove('hidden')
      saveButton.classList.add('hidden')
    }

  }
}