document.addEventListener('DOMContentLoaded', function () {
    const roleField = document.getElementById('id_role');
    const sellerField = document.getElementById('id_seller_name');

    function toggleSellerField() {
        if (roleField.value === 'seller') {
            sellerField.parentElement.style.display = 'flex';
        } else {
            sellerField.parentElement.style.display = 'none';
        }
    }

    toggleSellerField();
    roleField.addEventListener('change', toggleSellerField);
});