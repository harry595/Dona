document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('myBtn').addEventListener('click', () => {
    document.querySelector('.bg-modal').style.display ='flex';
    });
    document.getElementById('myBtn2').addEventListener('click', () => {
    document.querySelector('.bg-modal').style.display ='flex';
    });
    document.querySelector(".close").addEventListener('click',() => {
    document.querySelector('.bg-modal').style.display ='none';
    });
});