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
    const table = document.querySelector('.prodTable');

    const oldLines = table.querySelectorAll('.tdStyle');
    oldLines.forEach(line => line.remove());

    if(data.lenght <= 0) {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `<td class="tdStyle" colspan="6">Nenhum produto encontrado</td>`;
        table.appendChild(newLines);
        return;
    }

    data.forEach(item => {
        const newLines = document.createElement('tr');
        newLines.innerHTML = `
            <td class="tdStyle"><input type="checkbox" name="checkbox" value="${item.id}" class="checkboxStyle"></td>
            <td class="tdStyle"><img src="${imagePaths.placeholder}" alt="Foto" class="imgStyle"></td>
            <td class="tdStyle">${item.nome}</td>
            <td class="tdStyle">${item.categoria__nome}</td>
            <td class="tdStyle">R$ ${item.preco}</td>
            <td class="tdStyle">
                <img src="${imagePaths.edit}"
                    data-id="${item.id}"
                    alt="Editar" class="imgEdit">
                <img src="${imagePaths.delete}"
                    data-id="${item.id}"
                    data-nome="${item.nome}"
                alt="Excluir" class="imgDelete">
            </td>
        `;

        table.appendChild(newLines);
        addLinks();
    });
}

document.querySelector('.prodTable').addEventListener('click', (event) => {
    const element = event.target;

    if (element.classList.contains('imgDelete')) {
        currentId = element.getAttribute('data-id');
        const nome = element.getAttribute('data-nome');
        overlay.style.display = 'block';
        document.getElementById('modalDelete').style.display = 'block';
        document.getElementById('deleteMsg').innerHTML = `Tem certeza que deseja excluir o produto ${nome}?`;
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

function addLinks() {
    document.querySelectorAll('.imgEdit').forEach(img => {
        img.addEventListener('click', () => {
            const id = img.getAttribute('data-id');
            window.location.href = `/produto/detalhes/${id}`;
        });
    });
} 

document.getElementById('confirmDelete').addEventListener('click', () => {
    const deleteUrl = `/produto/deletar/${currentId}`;

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
            toastAlert('success', 'Produto excluído com sucesso');
            nextDataPage(currentPage);
        } else {
            console.error('Erro ao excluir produto', data);
            toastAlert('error', 'Erro ao excluir produto');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao excluir produto');
    });
});

function nextDataPage(page = 1) {
    const urlPage = `/produto/data/?page=${page}`;

    fetch(urlPage, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.produtos);
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

    let urlSearch = `/produtos/?search=${value}&page=${page}`;

    isSearching = true;

    fetch(urlSearch, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        addTableLines(data.Produtos);
        disableBtns(data.totalPages);
        searchPage = page;
        document.querySelector('.searchValue').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
        toastAlert('error', 'Erro ao buscar produtos');
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