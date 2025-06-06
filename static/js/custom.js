/* jshint esversion: 6 */
/* global bootstrap */

document.addEventListener("DOMContentLoaded", function () {
    'use strict';

    const toastElList = document.querySelectorAll('.toast');
    toastElList.forEach(function (toastEl) {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    });

    const telefoneInput = document.getElementById('id_telefone');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function () {
            let value = telefoneInput.value.replace(/\D/g, '');
            telefoneInput.value = value
                .replace(/^(\d{2})(\d{5})(\d{4})$/, '($1)$2-$3')
                .replace(/^(\d{2})(\d{4})(\d{4})$/, '($1)$2-$3');
        });
    }

    const usernameInput = document.getElementById('id_username');
    if (usernameInput) {
        usernameInput.addEventListener('input', function (e) {
            e.target.value = e.target.value.toLowerCase();
        });
    }
});
