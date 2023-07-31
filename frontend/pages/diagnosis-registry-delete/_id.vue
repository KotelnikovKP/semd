<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/diagnosis-registers">Список регистров ССЗ</nuxt-link>
                        </li>
                        <li class="breadcrumb-item active" aria-current="page">Удаление регистра {{ short_name }}</li>
                    </ol>
                </nav>

                <p class="lead">Подтвердите реестра:</p>

                <form name="diagnosis_registry_form" @submit.prevent="registryDelete">

                    <div class="row mt-3">
                        <div class="col-md-3">
                            <div class="md-form mb-0">
                                <label for="short_name">Краткое название</label>
                                <input type="text" id="short_name" rows="5" class="form-control"
                                    placeholder="Краткое название" v-model="short_name" readonly>
                            </div>
                        </div>
                        <div class="col-md-9">
                            <div class="md-form">
                                <label for="name">Название</label>
                                <input type="text" id="name" rows="5" class="form-control" placeholder="Название"
                                    v-model="name" readonly>
                            </div>
                        </div>
                    </div>

                    <br>
                    <p>Диагнозы в регистре:</p>
                    <table class="table table-striped table-bordered" id="registry_diagnoses_table">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Наименование</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(registry_diagnosis, index) in registry_diagnoses">
                                <td>{{ registry_diagnosis.diagnosis }}</td>
                                <td>{{ registry_diagnosis.diagnosis_name }}</td>
                            </tr>
                            <tr v-show="count_diagnoses == 0">
                                <td colspan="3">
                                    ...в регистре нет ни одного диагноза
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form">
                                <label for="err_msg" id="err_msg_lbl" class="fld-error-all"
                                    style="display: none">Ошибка</label>
                                <p class="lead fld-error-all" id="err_msg" style="display: none">Ошибка</p>
                            </div>
                        </div>
                    </div>

                    <div class="text-center text-md-left mt-3">
                        <button class="btn btn-primary" type="submit">Удалить</button>
                    </div>

                </form>
                <p> </p>

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
            count_diagnoses: 0,
            registry_diagnoses: [],
        }
    },
    async asyncData({ params }) {
        return {
            id: params.id,
        }
    },
    head() {
        return {
            title: "Удаление региста " + this.name,
        }
    },
    methods: {
        async getRegistryDiagnoses() {
            try {
                let registry = await this.$axios.get(`/api/v1/diagnosis_registry/${this.id}`);
                this.id = registry.data.result.id;
                this.short_name = registry.data.result.short_name;
                this.name = registry.data.result.name;
                let response = await this.$axios.get(`/api/v1/diagnosis_registry/${this.id}/diagnoses`);
                this.registry_diagnoses = response.data.result;
                this.count_diagnoses = response.data.retExtInfo.count_items;
            } catch ({ response }) {
                console.log(response);
            }
        },
        async registryDelete() {
            try {
                let response = await this.$axios.delete(`/api/v1/diagnosis_registry/${this.id}`);
                console.log(response);
                this.$router.push("/diagnosis-registers");
            } catch ({ response }) {
                console.log(response);
                const err = document.getElementById("err_msg");
                err.innerHTML = JSON.stringify(response.data);
                err.style.display = "";
                const err_lbl = document.getElementById("err_msg_lbl");
                err_lbl.innerHTML = "Error " + response.status + " (" + response.statusText + "):"
                err_lbl.style.display = "";
            }
        },
    },
    mounted() {
        this.getRegistryDiagnoses();
    },
}
</script>

<style type="text/css">
.fld-error-all {
    display: block;
    color: #dc3545;
}

.fld-error .msg-error {
    display: block;
    color: #dc3545;
}

.msg-error {
    display: none;
}
</style>
