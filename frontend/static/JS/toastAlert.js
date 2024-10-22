let activeToast = null;

function toastAlert(type, message) {
    if (activeToast) {
        activeToast.remove();
    }

    const toastAlert = document.createElement('div');
    toastAlert.classList.add('toastAlert');

    const progressBar = document.createElement('div');
    progressBar.style.height = '5px';
    progressBar.style.width = '100%';
    progressBar.style.transition = `width 3000ms linear`;

    if (type === 'success') {
        toastAlert.style.backgroundColor = '#2ECC71';
        toastAlert.style.border = '2px solid #C2D1BC';
        progressBar.style.backgroundColor = '#4CAF50';
    } else if (type === 'error') {
        toastAlert.style.backgroundColor = '#E14D45';
        toastAlert.style.border = '2px solid #B9A09D';
        progressBar.style.backgroundColor = '#921919';
    } else if (type === 'warn') {
        toastAlert.style.backgroundColor = '#F39C12';
        toastAlert.style.border = '2px solid #C2D1BC';
        progressBar.style.backgroundColor = '#c27809';
    }
    
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.style.padding = '10px';

    toastAlert.appendChild(messageElement);
    toastAlert.appendChild(progressBar);

    document.body.appendChild(toastAlert);

    setTimeout(() => {
        progressBar.style.width = '0';
    }, 100);

    setTimeout(() => {
        toastAlert.remove();
        if (activeToast === toastAlert) {
            activeToast = null;
        }
    }, 3000);

    activeToast = toastAlert;
}