document.addEventListener('DOMContentLoaded', function () {
    // Create arrays for committee and portfolio dropdowns
    var committeeDropdowns = document.querySelectorAll('select[name="committee"]');
    var portfolioDropdowns = document.querySelectorAll('select[name="portfolio"]');
  
    // Disable all portfolio dropdowns initially
    portfolioDropdowns.forEach(function (dropdown) {
      dropdown.disabled = true;
    });
  
    // Add event listeners for all committee dropdowns
    committeeDropdowns.forEach(function (committeeDropdown, index) {
      committeeDropdown.addEventListener('change', function () {
        var selectedCommittee = committeeDropdown.value;
        var correspondingPortfolioDropdown = portfolioDropdowns[index];
  
        if (selectedCommittee) {
          var xhr = new XMLHttpRequest();
          xhr.open('GET', '/get_options/?model_id=' + selectedCommittee, true);
          xhr.setRequestHeader('Content-Type', 'application/json');
          xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
              var data = JSON.parse(xhr.responseText);
              correspondingPortfolioDropdown.innerHTML = '<option value="" selected="">---------</option>';
              data.options.forEach(function (option) {
                var optionElement = document.createElement('option');
                optionElement.value = option.id;
                optionElement.text = option.name;
                correspondingPortfolioDropdown.appendChild(optionElement);
              });
              // Enable the corresponding portfolio dropdown when committee is selected
              correspondingPortfolioDropdown.disabled = false;
            }
          };
          xhr.send();
        } else {
          // If no committee is selected, disable and clear the corresponding portfolio dropdown
          correspondingPortfolioDropdown.disabled = true;
          correspondingPortfolioDropdown.innerHTML = '<option value="" selected="">---------</option>';
        }
      });
    });
  
    // Event listener for Enter key
    const inputElement = document.getElementById('id_text');
    inputElement.addEventListener('keydown', function (event) {
      if (event.key == "Enter") {
        event.preventDefault();
      }
    });
  });
  