<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/diagnosis-registers">Список регистров ССЗ</nuxt-link>
                        </li>
                        <li class="breadcrumb-item active" aria-current="page">Пациенты регистра {{ name }}</li>
                    </ol>
                </nav>

                <div class="row mt-3">
                    <div class="col-md-12">
                        <div class="md-form mb-2">
                            <form class="input-group search-form">
                                <input type="text" class="form-control" name="q" placeholder="Поиск по пациентам регистра"
                                    v-model="q">
                                <span class="input-group-btn ml-2">
                                    <button class="btn btn-secondary" @click.stop.prevent="fetchPage(1)"> Найти </button>
                                </span>
                            </form>
                        </div>
                    </div>
                </div>

                <div class="row" id="preloader" style="display: none">
                    <div class="col-md-12">
                        <img width="100em" src="/images/loading-1.gif" class="mx-auto d-block">
                    </div>
                </div>
                
               <table class="table table-striped table-bordered" id="registry_patients_table">
                    <thead>
                        <tr>
                            <th scope="col">СНИЛС</th>
                            <th scope="col">ФИО</th>
                            <th scope="col">Пол</th>
                            <th scope="col">Дата рождения</th>
                            <th scope="col">Диагнозы</th>
                            <th scope="col">Выписка</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="registry_patient in registry_patients" :key="registry_patient.snils">
                            <td>{{ registry_patient.snils.substr(0,3) }}-{{ registry_patient.snils.substr(3,3) }}-{{ registry_patient.snils.substr(6,3) }} {{ registry_patient.snils.substr(9,2) }}</td>
                            <td>{{ registry_patient.name }}</td>
                            <td>{{ registry_patient.gender }}</td>
                            <td>{{ Intl.DateTimeFormat().format(Date.parse(registry_patient.birthday)) }}</td>
                            <td>{{ registry_patient.diagnoses.reduce(function(sum, current) { return sum != "" ? sum + ", " + current.diagnosis_id : current.diagnosis_id }, "") }}</td>
                            <td width="1rem" data="Выписка" title="Выписка">
                                <nuxt-link :to="`/patient-registry-report/${registry_patient.snils}?registry=${id}`" class="btn btn-sm btn-outline-secondary">
                                    <img src="/images/document.png" class="image-table" alt="patient-card">
                                </nuxt-link>
                            </td>
                        </tr>
                    </tbody>
                </table>

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
                        <span v-for="i in [current_page-2, current_page-1, current_page, current_page+1, current_page+2]">
                            <li v-if="current_page === i" class="page-item ml-2 active">
                                <button class="page-link">{{ i }}</button>
                            </li>
                            <li v-else-if="(i >= current_page - 2) && (i <= current_page + 2) && (i > 0) && (i <= page_count)" class="page-item ml-2">
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
                                    v-model.number="searching_page" 
                                    @input="() => { if (searching_page < 1) searching_page = 1; if (searching_page > page_count) searching_page = page_count }">
                                <span class="input-group-btn ml-2">
                                    <button class="btn btn-primary" @click.stop.prevent="fetchPage(searching_page)"> Перейти </button>
                                </span>
                            </form>
                        </li>
                    </ul>
                </nav>

                <div class="row mt-3">
                    <div class="col-md-12">
                        <p class="lead">Найдено записей: {{ Intl.NumberFormat().format(count_items) }} (страниц: {{ Intl.NumberFormat().format(page_count) }})</p>
                    </div>
                </div>

            </div>
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
            id: 0,
            short_name: '',
            name: '',
            registry_patients: [],
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
    async asyncData({ params }) {
        return {
            id: params.id,
        }
    },
    head() {
        return {
            title: "Пациенты региста " + this.name,
        }
    },
    methods: {
        async fetchPage(p) {
            try {
                let preloader = document.getElementById("preloader");
                preloader.style.display = "";
                preloader.scrollIntoView();
                let registry = await this.$axios.get(`/api/v1/diagnosis_registry/${this.id}`);
                this.id = registry.data.result.id;
                this.short_name = registry.data.result.short_name;
                this.name = registry.data.result.name;
                let response = await this.$axios.get(`/api/v1/diagnosis_registry/${this.id}/patients?q=${this.q}&page=${p}`);
                this.registry_patients = response.data.result;
                this.count_items = response.data.retExtInfo.count_items;
                this.items_per_page = response.data.retExtInfo.items_per_page;
                this.start_item_index = response.data.retExtInfo.start_item_index;
                this.end_item_index = response.data.retExtInfo.end_item_index;
                this.previous_page = response.data.retExtInfo.previous_page;
                this.current_page = response.data.retExtInfo.current_page;
                this.searching_page = response.data.retExtInfo.current_page;
                this.next_page = response.data.retExtInfo.next_page;
                this.page_count = Math.ceil(response.data.retExtInfo.count_items / response.data.retExtInfo.items_per_page);
                preloader.style.display = "None";
            } catch ({ response }) {
                console.log(response);
                this.searching_page = this.current_page;
                preloader.style.display = "None";
            }
        },        
    },
    mounted() {
        this.fetchPage(1);
    },
}
</script>

<style type="text/css"></style>
