<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/diagnosis-registers">Список регистров ССЗ</nuxt-link>
                        </li>
                        <li class="breadcrumb-item"><nuxt-link :to="`/diagnosis-registry-patients/${registry_id}`">Пациенты
                                регистра {{ registry_name }}</nuxt-link>
                        </li>
                        <li class="breadcrumb-item active" aria-current="page">Выписка по пациенту {{ name }}</li>
                    </ol>
                </nav>

                <div class="row" id="preloader" style="display: none">
                    <div class="col-md-12">
                        <img width="100em" src="/images/loading-1.gif" class="mx-auto d-block">
                    </div>
                </div>

                <h4 class="my-3 text-danger">Пациент:</h4>
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

                <h4 class="my-3 text-danger">События:</h4>
                <table class="table table-striped table-bordered" id="events_table">
                    <thead>
                        <tr>
                            <th scope="col">Дата события</th>
                            <th scope="col">Тип события</th>
                            <th scope="col">Диагноз(ы)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="event in events" :key="event.internal_message_id">
                            <td><nuxt-link :to="`#`">{{ Intl.DateTimeFormat().format(Date.parse(event.service_time)) }}</nuxt-link></td>
                            <td>{{ event.document_type == '8' ? 'Выписной эпикриз из стационара' : event.medical_service_name }}</td>
                            <td>{{ event.diagnoses }}</td>
                        </tr>
                        <tr v-show="events.length == 0" :key="-1">
                            <td class="text-info" colspan="3">Увы! Ни одного события в СЭМДах по этому пациенту не найдено.</td>
                        </tr>
                    </tbody>
                </table>

                <h4 class="my-3 text-danger">Анализы:</h4>
                <table class="table table-striped table-bordered" id="medical_tests_table">
                    <thead>
                        <tr>
                            <th scope="col">Анализ</th>
                            <th scope="col">Дата</th>
                            <th scope="col">Значение</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="medical_test in medical_tests" :key="medical_test.id">
                            <td>{{ medical_test.laboratory_test_name }}</td>
                            <td><nuxt-link :to="`#`">{{ Intl.DateTimeFormat().format(Date.parse(medical_test.test_time)) }}</nuxt-link></td>
                            <td>{{ medical_test.value }}</td>
                        </tr>
                        <tr v-show="medical_tests.length == 0" :key="-1">
                            <td class="text-info" colspan="3">Увы! Ни одного анализа в СЭМДах по этому пациенту не найдено.</td>
                        </tr>
                    </tbody>
                </table>

                <h4 class="my-3 text-danger">Обследования:</h4>
                <table class="table table-striped table-bordered" id="medical_examinations_table">
                    <thead>
                        <tr>
                            <th scope="col">Обследование</th>
                            <th scope="col">Дата</th>
                            <th scope="col">Результат</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="medical_examination in medical_examinations" :key="medical_examination.internal_message_id">
                            <td>{{ medical_examination.medical_service_name }}:<br><b>{{ medical_examination.doctor }}</b><br>{{ medical_examination.medical_position_name }}<br>{{ medical_examination.medical_organization_name }}</td>
                            <td><nuxt-link :to="`#`">{{ Intl.DateTimeFormat().format(Date.parse(medical_examination.service_time)) }}</nuxt-link></td>
                            <td><b>Протокол:</b><br>{{ medical_examination.res_protocol }}<br><b>Заключение:</b><br>{{ medical_examination.res_conclusion }}<br><b>Диагноз:</b> {{ medical_examination.diagnoses }}</td>
                        </tr>
                        <tr v-show="medical_examinations.length == 0" :key="-1">
                            <td class="text-info" colspan="3">Увы! Ни одного обследования в СЭМДах по этому пациенту не найдено.</td>
                        </tr>
                    </tbody>
                </table>

                <h4 class="my-3 text-danger">Проведенное лечение:</h4>
                <table class="table table-striped table-bordered" id="treatments_table">
                    <thead>
                        <tr>
                            <th scope="col">Дата</th>
                            <th scope="col">Состав лечения</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="treatment in treatments" :key="treatment.internal_message_id">
                            <td><nuxt-link :to="`#`">{{ Intl.DateTimeFormat().format(Date.parse(treatment.service_time)) }}</nuxt-link></td>
                            <td>{{ treatment.res_recommendation }}</td>
                        </tr>
                        <tr v-show="treatments.length == 0" :key="-1">
                            <td class="text-info" colspan="3">Увы! Ни одного проведенного лечения в СЭМДах по этому пациенту не найдено.</td>
                        </tr>
                    </tbody>
                </table>

                <h4 class="my-3 text-danger">Рекомендованная терапия на последнем приеме:</h4>
                <table class="table table-striped table-bordered" id="recommended_therapies_table">
                    <thead>
                        <tr>
                            <th scope="col">Прием</th>
                            <th scope="col">Дата</th>
                            <th scope="col">Диагноз и рекомендации</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="recommended_therapy in recommended_therapies" :key="recommended_therapy.internal_message_id">
                            <td>{{ recommended_therapy.medical_service_name }}:<br><b>{{ recommended_therapy.doctor }}</b><br>{{ recommended_therapy.medical_position_name }}<br>{{ recommended_therapy.medical_organization_name }}</td>
                            <td><nuxt-link :to="`#`">{{ Intl.DateTimeFormat().format(Date.parse(recommended_therapy.service_time)) }}</nuxt-link></td>
                            <td><b>Диагноз:</b> {{ recommended_therapy.patient_diagnosis_id }} <b>Рекомендации:</b> {{ recommended_therapy.res_recommendation }}</td>
                        </tr>
                        <tr v-show="recommended_therapies.length == 0" :key="-1">
                            <td class="text-info" colspan="3">Увы! Ни одного приема специалиста в СЭМДах по этому пациенту не найдено.</td>
                        </tr>
                    </tbody>
                </table>

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
            snils: 0,
            snils_str: '',
            name: '',
            gender: '',
            birthday: '',
            birthday_str: '',
            diagnoses: [],
            diagnoses_str: '',
            medical_cards: [],
            registry_id: 0,
            registry_name: '',
            events: [],
            medical_tests: [],
            medical_examinations: [],
            treatments: [],
            recommended_therapies: [],
        }
    },
    async asyncData({ route }) {
        return {
            snils: route.params.snils,
            registry_id: route.query.registry,
        }
    },
    head() {
        return {
            title: "Выписка по пациенту " + this.name,
        }
    },
    methods: {
        async loadData() {
            try {
                let preloader = document.getElementById("preloader");
                preloader.style.display = "";
                // preloader.scrollIntoView();
                let registry = await this.$axios.get(`/api/v1/diagnosis_registry/${this.registry_id}`);
                this.registry_name = registry.data.result.short_name;
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
                let response = await this.$axios.get(`/api/v1/patient/${this.snils}/registry_report?diagnosis_registry_id=${this.registry_id}`);
                this.events = response.data.result.events;
                this.medical_tests = response.data.result.medical_tests;
                this.medical_examinations = response.data.result.medical_examinations;
                this.treatments = response.data.result.treatment;
                this.recommended_therapies = response.data.result.recommended_therapy;
                preloader.style.display = "None";
            } catch ({ response }) {
                console.log(response);
                preloader.style.display = "None";
            }
        },
    },
    mounted() {
        this.loadData();
    },
}
</script>

<style type="text/css"></style>
