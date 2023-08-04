<template>
    <div class="container">
        <h1 class="my-3">Список регистров ССЗ</h1>
        <div v-if="loggedIn">
            <div class="row mt-3">
                <div class="col-md-12">
                    <div class="md-form mb-2">
                        <form class="input-group search-form">
                            <input type="text" class="form-control" name="q" placeholder="Поиск по списку регистров ССЗ"
                                v-model="q">
                            <span class="input-group-btn ml-2">
                                <button class="btn btn-secondary" @click.stop.prevent="fetchPage(1)"> Найти </button>
                            </span>
                        </form>
                    </div>
                </div>
            </div>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Коротко</th>
                        <th scope="col">Наименование</th>
                        <th scope="col" colspan="3">Действия</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="diagnosis_registry in diagnosis_registers" :key="diagnosis_registry.id">
                        <td>{{ diagnosis_registry.id }}</td>
                        <td>{{ diagnosis_registry.short_name }}</td>
                        <td>{{ diagnosis_registry.name }}</td>
                        <td width="1rem" data="Пациенты" title="Пациенты">
                            <nuxt-link :to="`/diagnosis-registry-patients/${diagnosis_registry.id}`"
                                class="btn btn-sm btn-outline-secondary">
                                <img src="/images/patients.png" class="image-table" alt="edit">
                            </nuxt-link>
                        </td>
                        <td width="1rem" data="Изменить" title="Изменить">
                            <nuxt-link :to="`/diagnosis-registry-edit/${diagnosis_registry.id}`"
                                class="btn btn-sm btn-outline-secondary">
                                <img src="/images/edit.png" class="image-table" alt="edit">
                            </nuxt-link>
                        </td>
                        <td width="1rem" data="Удалить" title="Удалить">
                            <nuxt-link :to="`/diagnosis-registry-delete/${diagnosis_registry.id}`"
                                class="btn btn-sm btn-outline-secondary">
                                <img src="/images/delete.png" class="image-table" alt="delete">
                            </nuxt-link>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="row mt-3">
                <div class="col-md-12">
                    <div class="md-form mb-2">
                        <nuxt-link :to="`/diagnosis-registry-create`" class="btn btn-primary">Добавить регистр</nuxt-link>
                    </div>
                </div>
            </div>
            <nav aria-label="Paginate me">
                <ul class="pagination justify-content-center" ref="nav">
                    <button v-if="previous_page != null" class="page-link" @click="fetchPage(previous_page);"
                        tabindex="-1">Предыдущая</button>
                    <li v-else class="page-item disabled">
                        <a class="page-link disabled" href="#" tabindex="-1">Предыдущая</a>
                    </li>
                    <li v-if="current_page > 3" class="page-item ml-2 disabled">
                        <button class="page-link" style="border: 0">...</button>
                    </li>
                    <span v-for="i in [current_page - 2, current_page - 1, current_page, current_page + 1, current_page + 2]">
                        <li v-if="current_page === i" class="page-item ml-2 active">
                            <button class="page-link">{{ i }}</button>
                        </li>
                        <li v-else-if="(i >= current_page - 2) && (i <= current_page + 2) && (i > 0) && (i <= page_count)"
                            class="page-item ml-2">
                            <button class="page-link" @click="fetchPage(i);">{{ i }}</button>
                        </li>
                    </span>
                    <li v-if="current_page < page_count - 2" class="page-item ml-2 disabled">
                        <button class="page-link" style="border: 0">...</button>
                    </li>
                    <button v-if="next_page != null" class="page-link ml-2"
                        @click="fetchPage(next_page);">Следующая</button>
                    <li v-else class="page-item ml-2 disabled">
                        <a class="page-link" href="#">Следующая</a>
                    </li>
                    <li v-if="page_count > 3" class="page-item ml-2 disabled">
                        <button class="page-link" style="border: 0">№ стр.:</button>
                    </li>
                    <li v-if="page_count > 3" class="page-item ml-2 disabled">
                        <form class="input-group search-form">
                            <input type="text" class="form-control" style="width: 5em;" name="searching_page"
                                v-model="searching_page">
                            <span class="input-group-btn ml-2">
                                <button class="btn btn-primary" @click.stop.prevent="fetchPage(searching_page)"> Перейти
                                </button>
                            </span>
                        </form>
                    </li>
                </ul>
            </nav>
            <div class="row mt-3">
                <div class="col-md-12">
                    <p class="lead">Найдено записей: {{ count_items }}</p>
                </div>
            </div>
        </div>
        <div v-else>
            <h6 class="card-header"><nuxt-link to="/signin">Авторизуйтесь</nuxt-link> или <nuxt-link
                    to="/signup">зарегистрируйтесь</nuxt-link> для получения доступа к прототипам</h6>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import default_2826 from "@/layouts/default_2826";
export default {
    layout: "default_2826",
    data() {
        return {
            diagnosis_registers: [],
            count_items: 0,
            items_per_page: 0,
            start_item_index: 0,
            end_item_index: 0,
            previous_page: null,
            current_page: 1,
            searching_page: 1,
            next_page: null,
            page_count: 0,
            q: '',
        }
    },
    head() {
        return {
            title: "Список регистров ССЗ",
        }
    },
    methods: {
        async fetchPage(p) {
            if (this.loggedIn) {
                try {
                    let response = await this.$axios.get(`/api/v1/diagnosis_registry?q=${this.q}&page=${p}`);
                    this.diagnosis_registers = response.data.result;
                    this.count_items = response.data.retExtInfo.count_items;
                    this.items_per_page = response.data.retExtInfo.items_per_page;
                    this.start_item_index = response.data.retExtInfo.start_item_index;
                    this.end_item_index = response.data.retExtInfo.end_item_index;
                    this.previous_page = response.data.retExtInfo.previous_page;
                    this.current_page = response.data.retExtInfo.current_page;
                    this.next_page = response.data.retExtInfo.next_page;
                    this.page_count = Math.ceil(response.data.retExtInfo.count_items / response.data.retExtInfo.items_per_page);
                } catch ({ response }) {
                    console.log(response);
                }
            }
        },
    },
    mounted() {
        this.fetchPage(1);
    },
    computed: {
        loggedIn() {
            return this.$auth.loggedIn
        },
        user() {
            return this.$auth.user
        },
        token() {
            return this.$auth.strategy.token.get()
        }
    }
}
</script>

<style type="text/css"></style>
