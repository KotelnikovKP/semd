<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/patients">Пациенты</nuxt-link>
                        </li>
                        <li class="breadcrumb-item active" aria-current="page">СЭМДы по пациенту {{ name }}</li>
                    </ol>
                </nav>

                <h4 class="my-3">Пациент:</h4>
                <div class="row mt-3">
                    <div class="col-md-2">
                        <div class="md-form mb-0">
                            <label for="name">СНИЛС</label>
                            <input type="text" id="snils_str" rows="5" class="form-control" placeholder="СНИЛС"
                                v-model="snils_str" readonly>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="md-form">
                            <label for="name">ФИО</label>
                            <input type="text" id="name" rows="5" class="form-control" placeholder="ФИО"
                                v-model="name" readonly>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="md-form mb-0">
                            <label for="name">Дата рождения</label>
                            <input type="text" id="birthday_str" rows="5" class="form-control" placeholder="Дата рождения"
                                v-model="birthday_str" readonly>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="md-form mb-0">
                            <label for="name">Пол</label>
                            <input type="text" id="gender" rows="5" class="form-control" placeholder="Пол"
                                v-model="gender" readonly>
                        </div>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-12">
                        <div class="md-form mb-0">
                            <label for="name">Диагнозы</label>
                            <input type="text" id="diagnoses_str" rows="5" class="form-control" placeholder="Диагнозы"
                                v-model="diagnoses_str" readonly>
                        </div>
                    </div>
                </div>

                <h4 class="my-3">СЭМДы:</h4>
 
                <div class="row mt-3">
                    <div class="col-md-12">
                        <div class="md-form mb-2">
                            <form class="input-group search-form">
                                <input type="text" class="form-control" name="q" placeholder="Поиск по СЭМДам"
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
 
                <table class="table table-striped table-bordered" id="semds_table">
                    <thead>
                        <tr>
                            <th scope="col">Дата</th>
                            <th scope="col">Тип</th>
                            <th scope="col">Событие</th>
                            <th scope="col">Диагноз(ы)</th>
                            <th scope="col">Где</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="semd in semds" :key="semd.internal_message_id">
                            <td><nuxt-link :to="`#`">{{ Intl.DateTimeFormat().format(Date.parse(semd.service_time)) }}</nuxt-link><br><br>{{ semd.internal_message_id }}</td>
                            <td>{{ semd.document_type }}</td>
                            <td>{{ semd.document_type == '8' ? 'Выписной эпикриз из стационара' : semd.medical_service_name }}</td>
                            <td>{{ semd.diagnoses }}</td>
                            <td>{{ semd.doctor }}<br>{{ semd.medical_position_name }}<br>{{ semd.medical_organization_name }}</td>
                        </tr>
                        <tr v-show="semds.length == 0" :key="-1">
                            <td colspan="5">Увы! Ни одного СЭМДа по этому пациенту не найдено.</td>
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

export default {
    data() {
        return {
            snils: 0,
            snils_str: '',
            name: '',
            gender: '',
            birthday: '',
            birthday_str: '',
            diagnoses: [],
            diagnoses_str: '',
            medical_cards: [],
            semds: [],
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
            snils: params.snils,
        }
    },
    head() {
        return {
            title: "СЭМДы по пациенту " + this.name,
        }
    },
    methods: {
        async fetchPage(p) {
            try {
                let preloader = document.getElementById("preloader");
                preloader.style.display = "";
                preloader.scrollIntoView();
                let patient = await this.$axios.get(`/api/v1/patient/${this.snils}`);
                this.snils = patient.data.result.snils;
                this.snils_str = this.snils.substr(0,3) + '-' + this.snils.substr(3,3) + '-' + this.snils.substr(6,3) + ' ' + this.snils.substr(9,2);
                this.name = patient.data.result.name;
                this.gender = patient.data.result.gender;
                this.birthday = patient.data.result.birthday;
                this.birthday_str = Intl.DateTimeFormat().format(Date.parse(this.birthday));
                this.diagnoses = patient.data.result.diagnoses;
                this.diagnoses_str = this.diagnoses.reduce(function (sum, current) { return sum != "" ? sum + ", " + current.diagnosis_id : current.diagnosis_id }, "")
                this.medical_cards = patient.data.result.medical_cards;
                let response = await this.$axios.get(`/api/v1/patient/${this.snils}/semds?q=${this.q}&page=${p}`);
                this.semds = response.data.result;
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
