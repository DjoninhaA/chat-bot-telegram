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
    const table = document.querySelector('.catTable');

    const oldLines = table.querySelectorAll('.tdStyle');
    oldLines.forEach(line => line.remove());

    if(data.length <= 0) {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `<td class="tdStyle" colspan="4">Nenhuma categoria encontrada</td>`;
        table.appendChild(newLines);
        return;
    }

    data.forEach(item => {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `
            <td class="tdStyle">${item.nome}</td>
            <td class="tdStyle">${item.descricao || ''}</td>
            <td class="tdStyle">${item.criado_em}</td>
            <td class="tdStyle">
                <img src="${imagePaths.edit}"
                    data-id="${item.id}"
                    data-nome="${item.nome}"
                    data-descricao="${item.descricao || ''}"
                    alt="Editar" class="imgEdit">
                <img src="${imagePaths.delete}"
                    data-id="${item.id}"
                    data-nome="${item.nome}"
                alt="Excluir" class="imgDelete">
            </td>
        `;

        table.appendChild(newLines);
    });
}

document.querySelector('.catTable').addEventListener('click', (event) => {
    const element = event.target;

    if (element.classList.contains('imgDelete')) {
        currentId = element.getAttribute('data-id');
        const nome = element.getAttribute('data-nome');
        overlay.style.display = 'block';
        document.getElementById('modalDelete').style.display = 'block';
        document.getElementById('deleteMsg').innerText = `Tem certeza que deseja excluir a categoria \n ${nome}?`;
    }

    if (element.classList.contains('imgEdit')) {
        currentId = element.getAttribute('data-id');
        overlay.style.display = 'block';
        document.getElementById('modalEdit').style.display = 'block';
        document.getElementById('nomeEdit').value = element.getAttribute('data-nome');
        document.getElementById('descricaoEdit').value = element.getAttribute('data-descricao');
    }
});

overlay.addEventListener('click', () => {
    overlay.style.display = 'none';
    document.getElementById('modalDelete').style.display = 'none';
    document.getElementById('modalEdit').style.display = 'none';
    document.getElementById('modalAdd').style.display = 'none';
});

document.querySelectorAll('btnsCancel').forEach(btn => btn.addEventListener('click', () => {
    overlay.style.display = 'none';
    document.getElementById('modalDelete').style.display = 'none';
    document.getElementById('modalEdit').style.display = 'none';
    document.getElementById('modalAdd').style.display = 'none';
}));

document.querySelector('.addCat').addEventListener('click', () => {
    overlay.style.display = 'block';
    document.getElementById('modalAdd').style.display = 'block';
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

document.getElementById('confirmAdd').addEventListener('click', () => {
    const nome = document.getElementById('nome').value;
    const descricao = document.getElementById('descricao').value;

    if (nome === '') {
        toastAlert('error', 'Nome da categoria é obrigatório');
        return;
    }

    const addUrl = `/produto/categoria/criar/`;

    fetch(addUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nome: nome,
            descricao: descricao
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.message) {
            overlay.style.display = 'none';
            document.getElementById('modalAdd').style.display = 'none';
            document.getElementById('nome').value = '';
            document.getElementById('descricao').value = '';
            toastAlert('success', 'Categoria adicionada com sucesso');
            nextDataPage(currentPage);
        } else {
            console.error('Erro ao adicionar categoria', data);
            toastAlert('error', 'Erro ao adicionar categoria');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao adicionar categoria');
    });
});

document.getElementById('confirmEdit').addEventListener('click', () => {
    const nome = document.getElementById('nomeEdit').value;
    const descricao = document.getElementById('descricaoEdit').value;

    if (nome === '') {
        toastAlert('error', 'Nome da categoria é obrigatório');
        return;
    }

    const editUrl = `/produto/categoria/editar/${currentId}`;

    fetch(editUrl, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nome: nome,
            descricao: descricao
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.message) {
            overlay.style.display = 'none';
            document.getElementById('modalEdit').style.display = 'none';
            toastAlert('success', 'Categoria editada com sucesso');
            nextDataPage(currentPage);
        } else {
            console.error('Erro ao editar categoria', data);
            toastAlert('error', 'Erro ao editar categoria');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao editar categoria');
    });
});

document.getElementById('confirmDelete').addEventListener('click', () => {
    const deleteUrl = `/produto/categoria/deletar/${currentId}`;

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
            toastAlert('success', 'Categoria excluída com sucesso');
            nextDataPage(currentPage);
        } else {
            console.error('Erro ao excluir categoria', data);
            toastAlert('error', 'Erro ao excluir categoria');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao excluir categoria');
    });
});

function nextDataPage(page = 1) {
    const urlPage = `/produto/categoria/data`;

    fetch(urlPage, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.categorias);
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

    let urlSearch = `/produto/categoria/search/?query=${value}`;

    isSearching = true;

    fetch(urlSearch, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.categorias);
        disableBtns(data.totalPages);
        searchPage = page;
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao buscar categorias');
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