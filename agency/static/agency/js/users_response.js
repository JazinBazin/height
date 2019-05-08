'use strict';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

openResponseFormBtn.addEventListener('click', function () {
    popUpContainer.hidden = false;
})

closePopUpBtn.addEventListener('click', function () {
    popUpContainer.hidden = true;
})

popUpContainer.addEventListener('click', function (event) {
    if (!popUpContent.contains(event.target))
        popUpContainer.hidden = true;
})

function checkField(field, fieldErrors) {
    if (!field.checkValidity()) {
        fieldErrors.textContent = field.validationMessage;
        fieldErrors.hidden = false;
        return false;
    }
    else {
        fieldErrors.hidden = true;
        return true;
    }
}

function switchLoadingSpinner() {
    usersResponseBtn.hidden = !usersResponseBtn.hidden;
    loadingSpinner.hidden = !loadingSpinner.hidden;
}

usersResponseBtn.addEventListener('click', function () {
    var responseForm = document.forms['adResponseForm'];
    if (checkField(responseForm.elements['users_name'], nameErrors) &&
        checkField(responseForm.elements['users_phone'], phoneErrors) &&
        checkField(responseForm.elements['users_email'], emailErrors)) {
        switchLoadingSpinner();
        var formData = {};
        for (var i = 0; i < responseForm.elements.length; ++i) {
            var fieldName = responseForm.elements[i].name;
            var fieldValue = responseForm.elements[i].value
            formData[fieldName] = fieldValue;
        }
        axios.post('/user_response/', {
            vendorCode: vendorCode,
            formData: formData,
        }
        ).then(function (response) {
            var status = response.data;
            if (status == 'ok') {
                popUpContainer.hidden = true;
                setTimeout(function () {
                    successMessageContainer.hidden = false;
                }, 0);
            }
            else {
                alert("Не удалось отправить отклик.\nПопробуйте позже.");
            }
            switchLoadingSpinner()
        }).catch(function (error) {
            alert("Не удалось отправить отклик.\nПопробуйте позже.");
            switchLoadingSpinner();
        })
    }
})

successMessageCloseBtn.addEventListener('click', function () {
    successMessageContainer.hidden = true;
})