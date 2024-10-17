// Function to show the alert message with animation
function showAlertMessage() {
    const alertMessage = document.getElementById("alertMessage");
    alertMessage.classList.remove("d-none");
    alertMessage.classList.add("show");
  }
  
  // Function to hide the alert message
  function hideAlertMessage() {
    const alertMessage = document.getElementById("alertMessage");
    alertMessage.classList.add("d-none");
    alertMessage.classList.remove("show");
  }
  
  // Function to handle register button click
  function submitBloodBankForm() {
    // Perform registration logic here
    // For demonstration purposes, let's just show the alert message
    showAlertMessage();
  }
  