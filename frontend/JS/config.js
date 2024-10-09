function sendConfig() {
    const urlConfig = '/config'
    const botName = document.getElementById('botName').value.trim();
    const botDesc = document.getElementById('botDesc').value.trim();

    if(!botName) {
        toastAlert('warn', 'O nome do bot é obrigatório!');
        return;
    }

    fetch(urlConfig, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ botName, botDesc }),
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            toastAlert('success', data.message);
            window.location.href = '/produtos';
        } else {
            console.log(data);
            toastAlert('error', 'Erro ao configurar seu bot!');
        }
    })
    .catch((error) => {
        console.error('Erro ao criar o bot: ', error);
        toastAlert('error', 'Erro ao configurar seu bot!');
    });
}

document.getElementById('sendBtn').addEventListener('click', () => {
    sendConfig()
});

document.getElementById('botName').addEventListener('keypress', (e) => {
    if(e.key === 'Enter') {
        sendConfig()
    }
});

document.getElementById('botDesc').addEventListener('keypress', (e) => {
    if(e.key === 'Enter') {
        sendConfig()
    }
});