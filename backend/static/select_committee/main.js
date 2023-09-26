console.log("testing");

const preferenceForm = document.getElementById("preference-form");
const committeeDataBox = document.getElementById("committees-data-box");
const committeeInput = document.getElementById("committees");

const portfolioDataBox = document.getElementById("portfolios-data-box");
const portfolioInput = document.getElementById("portfolios");

const portfolioText = document.getElementById("portfolio-text");
const committeeText = document.getElementById("portfolio-text");

const alertBox = document.getElementById("alert-box");

const csrf = document.getElementsByName("csrfmiddlewaretoken");

$.ajax({
  type: "GET",
  url: "/committee-json/",
  success: function (response) {
    console.log(response.data);
    const committeeData = response.data;
    committeeData.map((item) => {
      const option = document.createElement("option");
      option.textContent = item.committee; //change
      option.setAttribute("class", "item");
      option.setAttribute("data-value", item.committee); //change
      committeeDataBox.appendChild(option);
    });
  },
  error: function (err) {
    console.log(err);
  },
});

committeeInput.addEventListener("change", (e) => {
  console.log("changed");
  const selectedCommittee = e.target.value;

  alertBox.innerHTML = "";
  portfolioDataBox.innerHTML = "";
  portfolioText.textContent = "Select Portfolio";
  portfolioText.classList.add("default-portfolio");

  $.ajax({
    type: "GET",
    url: `/portfolio-json/${selectedCommittee}`,
    success: function (response) {
      console.log(response.data);
      const portfolioData = response.data;
      portfolioData.map((item) => {
        const option = document.createElement("option");
        option.textContent = item.portfolio; //change
        option.setAttribute("class", "item");
        option.setAttribute("data-value", item.portfolio); //change
        portfolioDataBox.appendChild(option);
      });
    },
    error: function (err) {
      console.log(err);
    },
  });
});

preferenceForm.addEventListener("submit", (e) => {
  e.preventDefault();
  console.log("submmitted");

  $.ajax({
    type: "POST",
    url: "/post-preference/",
    data: {
      csrfmiddlewaretoken: csrf[0].value,
      committee: committeeText.textContent,
      portfolio: portfolioText.textContent,
    },
    success: function (response) {
      console.log(response);
      alertBox.innerHTML = `<div>
      <h1>positvie</h1>
      </div>`;
    },
    error: function (err) {
      console.log(err);
      alertBox.innerHTML = `<div>
      <h1>negative</h1>
      </div>`;
    },
  });
});
