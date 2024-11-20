const priorBtn = document.getElementById('priorBtn');
const nextBtn = document.getElementById('nextBtn');
var currentPage = 1;
var searchPage = 1;
let isSearching = false;
let currentId;

document.addEventListener('DOMContentLoaded', () => {
    nextDataPage();
});

function addTableLines(data) {
    const table = document.querySelector('.pedTable');

    const oldLines = table.querySelectorAll('.tdStyle');
    oldLines.forEach(line => line.remove());

    if(data.length <= 0) {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `<td class="tdStyle" colspan="5">Nenhum pedido encontrado</td>`;
        table.appendChild(newLines);
        return;
    }

    data.forEach(item => {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `
            <td class="tdStyle">#${item.id}</td>
            <td class="tdStyle"><div class="divStatus">
                <span class="spanStatus ${item.status}" 
                data-status="${item.status}" data-id="${item.id}"
                >${item.status}</span>
            </div></td>
            <td class="tdStyle">R$${item.valor}</td>
            <td class="tdStyle">${item.cliente}</td>
            <td class="tdStyle">
                <img src="${imagePaths.edit}"
                    data-id="${item.id}"
                alt="Editar" class="imgEdit">
            </td>
        `;

        table.appendChild(newLines);
    });
}

document.querySelector('.pedTable').addEventListener('click', (event) => {
    if (event.target.classList.contains('spanStatus')) {
        const currentId = event.target.getAttribute('data-id');
        let status = event.target.getAttribute('data-status');

        let newStatus;

        if (status === 'Aguardando') {
            newStatus = 1;
        } else if (status === 'Preparando') {
            newStatus = 2;
        } else if (status === 'Pronto') {
            newStatus = 3;
        } else if (status === 'Entregue') {
            newStatus = 0;
        } else if (status === 'CANCELADO') {
            toastAlert('error', 'Pedido cancelado não pode ser alterado');
            return;
        } else {
            toastAlert('error', 'Status desconhecido');
            console.error('Status desconhecido:', status);
            return;
        }

        fetch(`/pedido/alterarStatus/${currentId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus }),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Falha ao alterar status');
            }
            return response.json();
        })
        .then((data) => {
            event.target.classList.remove('Aguardando', 'Preparando', 'Pronto', 'Entregue');

            event.target.innerText = data.status;
            event.target.setAttribute('data-status', data.status);

            event.target.classList.add(data.status);
        })
        .catch((error) => {
            console.error('Error:', error);
            toastAlert('error', 'Erro ao alterar status');
        });
    }
});

document.querySelector('.searchImg').addEventListener('click', () => {
    searchData();
});

document.getElementById('searchValue').addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
        searchData();
    }
});

nextBtn.addEventListener('click', () => {
    if (isSearching) {
        searchPage++;
        searchData(searchPage);
    } else {
        currentPage++;
        nextDataPage(currentPage);
    }
});

priorBtn.addEventListener('click', () => {
    if (isSearching) {
        searchPage--;
        if (searchPage < 1) searchPage = 1;
        searchData(searchPage);
    } else {
        currentPage--;
        if (currentPage < 1) currentPage = 1;
        nextDataPage(currentPage);
    }
});

document.getElementById('searchValue').addEventListener('input', () => {
    if(document.getElementById('searchValue').value === '') {
        isSearching = false;
        currentPage = 1;
        nextDataPage(currentPage);
    }
});

function nextDataPage(page = 1) {
    const urlPage = `/pedido/data/?page=${page}`;

    fetch(urlPage, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.pedidos);
        disableBtns(data.totalPages);
        currentPage = page;
    })
    .catch(error => console.error('Error:', error));
}

function searchData(page = 1) {
    const value = document.getElementById('searchValue').value;

    if (value === '') {
        isSearching = false;
        nextDataPage();
        return;
    }

    let urlSearch = `/pedido/search/?query=${value}&page=${page}`;

    isSearching = true;

    fetch(urlSearch, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.pedidos);
        disableBtns(data.totalPages);
        searchPage = page;
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao buscar pedidos');
    })
}

function disableBtns(totalPages) {
    if (isSearching) {
        if (searchPage <= 1) {
            priorBtn.classList.add('disabledBtn');
        } else {
            priorBtn.classList.remove('disabledBtn');
        }

        if (searchPage >= (totalPages)) {
            nextBtn.classList.add('disabledBtn');
        } else {
            nextBtn.classList.remove('disabledBtn');
        }
    } else {
        if (currentPage <= 1) {
            priorBtn.classList.add('disabledBtn');
        } else {
            priorBtn.classList.remove('disabledBtn');
        }

        if (currentPage >= (totalPages)) {
            nextBtn.classList.add('disabledBtn');
        } else {
            nextBtn.classList.remove('disabledBtn');
        }
    }
}