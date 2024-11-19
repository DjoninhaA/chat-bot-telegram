const overlay = document.getElementById('overlay');
const addBtn = document.getElementById('addBtn');
const editBtn = document.getElementById('editBtn');
if(document.getElementById('idProduto')) var currentId = document.getElementById('idProduto').value;

overlay.addEventListener('click', () => {
    overlay.style.display = 'none';
    document.querySelector('.modalCategoria').style.display = 'none';
    document.getElementById('cadCategoria').value = '';
});

document.getElementById('btnCategoria').addEventListener('click', () => {
    overlay.style.display = 'block';
    document.querySelector('.modalCategoria').style.display = 'flex';
});

document.getElementById('addImg').addEventListener('click', () => {
    document.getElementById('imagemInput').click();
});

document.getElementById('imagemInput').addEventListener('change', () => {
    const file = document.getElementById('imagemInput').files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
        document.querySelector('.imgProduto').src = reader.result;
    }

    if(file) {
        reader.readAsDataURL(file);
    }
});

if (addBtn) {
    addBtn.addEventListener('click', () => {
        const urlAdd = '/produto/criar/';

        const imagem = document.getElementById('imagemInput').files[0];
        const nome = document.getElementById('nome').value;
        const descricao = document.getElementById('descricao').value;
        const categoria = document.getElementById('categoria').value;
        const subcategoria = document.getElementById('subCategoria').value;
        const preco = document.getElementById('preco').value;
        const tempoDePreparo = document.getElementById('tempo').value;

        console.log(imagem)

        if (!nome || !descricao || !categoria || !subcategoria || !preco || !tempoDePreparo) {
            toastAlert('warn', 'Preencha todos os campos!');
            return;
        }

        const formData = new FormData();
        formData.append('imagem', imagem);
        formData.append('nome', nome);
        formData.append('descricao', descricao);
        formData.append('categoria', categoria);
        formData.append('subcategoria', subcategoria);
        formData.append('preco', preco);
        formData.append('tempoDePreparo', tempoDePreparo);

        fetch(urlAdd, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                toastAlert('success', 'Produto cadastrado com sucesso!');
                document.getElementById('nome').value = '';
                document.getElementById('descricao').value = '';
                document.getElementById('subCategoria').value = '';
                document.getElementById('preco').value = '';
                document.getElementById('tempo').value = '';
                document.getElementById('imagemInput').value = '';
            } else {
                console.error(data);
                toastAlert('error', data.error);
            }
        })
        .catch(error => {
            console.error('Erro ao cadastrar produto', error);
            toastAlert('error', 'Erro ao cadastrar produto');
        });
    });
}

if(editBtn) {
    editBtn.addEventListener('click', () => {
        const urlEdit = `/produto/editar/${currentId}`;

        const imagem = document.getElementById('imagemInput').files[0];
        const nome = document.getElementById('nome').value;
        const descricao = document.getElementById('descricao').value;
        const categoria = document.getElementById('categoria').value;
        const subcategoria = document.getElementById('subCategoria').value;
        const preco = document.getElementById('preco').value;
        const tempoDePreparo = document.getElementById('tempo').value;

        if(!nome || !descricao || !categoria || !subcategoria || !preco || !tempoDePreparo) {
            toastAlert('warn','Preencha todos os campos!');
            return;
        }

        fetch(urlEdit, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                imagem,
                nome,
                descricao,
                categoria,
                subcategoria,
                preco,
                tempoDePreparo
            })
        })
        .then(response => response.json())
        .then(data => {
            if(data.message) {
                toastAlert('success', 'Produto editado com sucesso!');
            } else {
                console.error(data);
                toastAlert('error', data.error);
            }
        })
        .catch(error => {
            console.error('Erro ao editar produto', error);
            toastAlert('error', 'Erro ao editar produto');
        });
    });
}

document.getElementById('addCategoria').addEventListener('click', () => {
    const urlAddCategoria = '/produto/categoria/criar/';

    const nome = document.getElementById('cadCategoria').value;

    if(!nome) {
        toastAlert('warn','Preencha o campo!');
        return;
    }

    fetch(urlAddCategoria, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({nome})
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            toastAlert('success', 'Categoria cadastrada com sucesso!');
            overlay.style.display = 'none';
            document.querySelector('.modalCategoria').style.display = 'none';
            document.getElementById('cadCategoria').value = '';
            document.getElementById('categoria').innerHTML += `<option value="${data.categoriaId}">${data.categoriaNome}</option>`;
            document.getElementById('categoria').value = data.categoriaId;
        } else {
            console.error(data);
            toastAlert('error', data.error);
        }
    })
    .catch(error => {
        console.error('Erro ao cadastrar categoria', error);
        toastAlert('error', 'Erro ao cadastrar categoria');
    });
});