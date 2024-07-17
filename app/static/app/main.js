window.addEventListener('beforeunload', function() {
    localStorage.setItem('scrollPosition', window.scrollY);
});

// Funkcja do przywracania pozycji scrolla po ponownym załadowaniu strony
window.addEventListener('load', function() {
    var scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition !== null) {
        window.scrollTo(0, parseInt(scrollPosition));
        localStorage.removeItem('scrollPosition');
    }
});

function descResize() {
    const textarea = document.getElementById('description_text');
    if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';

    }
}

document.addEventListener('DOMContentLoaded', function() {
    descResize();
    const textarea = document.getElementById('description_text');
    if (textarea) {
        textarea.addEventListener('input', descResize);
        textarea.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                document.getElementById('description_form').submit();
            }
        });
    }
    const userInput = document.getElementById("userInput");
    if (userInput){
        userInput.focus();
    }
    const loginUsernameField = document.getElementById("usernameLoginField");
    if (loginUsernameField){
        loginUsernameField.focus();
    }
});