const priorBtn = document.getElementById('priorBtn');
const nextBtn = document.getElementById('nextBtn');
const overlay = document.getElementById('overlay');
var currentPage = 1;
var searchPage = 1;
let isSearching = false;
let currentId;

document.addEventListener('DOMContentLoaded', () => {
    nextDataPage();
});

function addTableLines(data) {
    console.log(data);
    const table = document.querySelector('.userTable');

    const oldLines = table.querySelectorAll('.tdStyle');
    oldLines.forEach(line => line.remove());

    if(data.length <= 0) {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `<td class="tdStyle" colspan="4">Nenhum usuario encontrado</td>`;
        table.appendChild(newLines);
        return;
    }

    data.forEach(item => {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `
            <td class="tdStyle">${item.username}</td>
            <td class="tdStyle">${item.email}</td>
            <td class="tdStyle">Administrador</td>
            <td class="tdStyle">
                <img src="${imagePaths.delete}"
                    data-id="${item.id}"
                    data-nome="${item.username}"
                alt="Excluir" class="imgDelete">
            </td>
        `;

        table.appendChild(newLines);
    });
}

document.querySelector('.userTable').addEventListener('click', (event) => {
    const element = event.target;

    if (element.classList.contains('imgDelete')) {
        currentId = element.getAttribute('data-id');
        const nome = element.getAttribute('data-nome');
        overlay.style.display = 'block';
        document.getElementById('modalDelete').style.display = 'block';
        document.getElementById('deleteMsg').innerHTML = `Tem certeza que deseja excluir o usuário ${nome}?`;
    }
});

overlay.addEventListener('click', () => {
    overlay.style.display = 'none';
    document.getElementById('modalDelete').style.display = 'none';
});

document.getElementById('cancelDelete').addEventListener('click', () => {
    overlay.style.display = 'none';
    document.getElementById('modalDelete').style.display = 'none';
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

document.getElementById('confirmDelete').addEventListener('click', () => {
    const deleteUrl = `/usuario/deletar/${currentId}`;

    fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.message) {
            overlay.style.display = 'none';
            document.getElementById('modalDelete').style.display = 'none';
            toastAlert('success', 'Usuário excluído com sucesso');
            nextDataPage(currentPage);
        } else {
            console.error('Erro ao excluir usuario', data);
            toastAlert('error', 'Erro ao excluir usuario');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao excluir usuario');
    });
});

function nextDataPage(page = 1) {
    const urlPage = `/usuario/data/?page=${page}`;

    fetch(urlPage, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.usuarios);
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

    let urlSearch = `/usuario/search/?query=${value}&page=${page}`;

    isSearching = true;

    fetch(urlSearch, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.usuarios);
        disableBtns(data.totalPages);
        searchPage = page;
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao buscar usuarios');
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