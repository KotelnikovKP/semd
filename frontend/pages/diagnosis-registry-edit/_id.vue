<template>
    <div class="container">
        <div class="row">
            <div class="col-lg-12">

                <nav aria-label="breadcrumb" class="mt-4">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><nuxt-link to="/diagnosis-registers">Список регистров ССЗ</nuxt-link>
                        </li>
                        <li class="breadcrumb-item active" aria-current="page">Изменение регистра {{ short_name }}</li>
                    </ol>
                </nav>

                <form name="diagnosis_registry_form" @submit.prevent="registryUpdate">

                    <div class="row mt-3">
                        <div class="col-md-3" v-bind:class="{ 'fld-error': $v.short_name.$error }">
                            <div class="md-form mb-0">
                                <label for="short_name">Краткое название</label>
                                <input type="text" id="short_name" rows="5" class="form-control"
                                    placeholder="Краткое название" v-model="short_name" @input="$v.short_name.$touch()">
                            </div>
                            <span class="msg-error" v-if="!$v.short_name.required">
                                <small>Поле обязательно для заполнения</small>
                            </span>
                            <span class="msg-error" v-if="!$v.short_name.maxLength">
                                <small>Должно быть не больше {{ $v.short_name.$params.maxLength.max }}
                                    символов.</small>
                            </span>
                        </div>
                        <div class="col-md-9" v-bind:class="{ 'fld-error': $v.name.$error }">
                            <div class="md-form">
                                <label for="name">Название</label>
                                <input type="text" id="name" rows="5" class="form-control" placeholder="Название"
                                    v-model="name" @input="$v.name.$touch()">
                            </div>
                            <span class="msg-error" v-if="!$v.name.required">
                                <small>Поле обязательно для заполнения</small>
                            </span>
                            <span class="msg-error" v-if="!$v.name.maxLength">
                                <small>Должно быть не больше {{ $v.name.$params.maxLength.max }}
                                    символов.</small>
                            </span>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-12">
                            <div class="md-form">
                                <label for="medical_record_transcript_settings">Настройки выписки пациента реестра</label>
                                <textarea type="text" id="medical_record_transcript_settings" rows="10"
                                    class="form-control md-textarea" placeholder="Настройки выписки пациента реестра"
                                    v-model="medical_record_transcript_settings"
                                    @input="onJSONChange"></textarea>
                            </div>
                        </div>
                    </div>
                    <div class="text-danger" v-if="!isJSONValid"><small>Неверный формат JSON: {{ JSONerr }}</small></div>

                    <br>
                    <p>Диагнозы в регистре:</p>
                    <table class="table table-striped table-bordered" id="registry_diagnoses_table">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Наименование</th>
                                <th scope="col" width="1rem">Del</th>
                            </tr>
                            <tr>
                                <th scope="col" colspan="3">
                                    <div class="md-form mb-0">
                                        <input type="text" id="diagnosis_name" class="form-control"
                                            placeholder="Введите код или наименование диагноза для добавления в регистр"
                                            v-model="diagnosis_name" @input="onChange">
                                    </div>
                                    <ul class="list-group" name="diagnosis_list" v-show="isOpen">
                                        <button class="list-group-item list-group-item-action"
                                            v-for="diagnosis in diagnoses" :key="diagnosis.mkb_code"
                                            @click.prevent="setResult(diagnosis.mkb_code, diagnosis.name)" tabindex="-1">
                                            {{ diagnosis.mkb_code }} {{ diagnosis.name }}
                                        </button>
                                        <button class="list-group-item list-group-item-action"
                                            v-show="count_founded_diagnoses == 0" :key="-1" tabindex="-1" disabled>
                                            Ничего не найдено
                                        </button>
                                        <button class="list-group-item list-group-item-action"
                                            v-show="count_founded_diagnoses > 10" :key="-2" tabindex="-1" disabled>
                                            ...всего найдено {{ count_founded_diagnoses }} диагнозов
                                        </button>
                                    </ul>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(registry_diagnosis, index) in registry_diagnoses">
                                <td>{{ registry_diagnosis.diagnosis }}</td>
                                <td>{{ registry_diagnosis.diagnosis_name }}</td>
                                <td width="1rem" data="Удалить" title="Удалить">
                                    <button @click.stop.prevent="removeItem(index)"
                                        class="btn btn-sm btn-outline-secondary">
                                        <img src="/images/delete.png" class="image-table" alt="delete">
                                    </button>
                                </td>
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
                        <button class="btn btn-primary" type="submit" :disabled="!isComplete">Обновить</button>
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
import { required, maxLength } from 'vuelidate/lib/validators'

export default {
    layout: "default_2826",
    data() {
        return {
            id: 0,
            short_name: '',
            name: '',
            medical_record_transcript_settings: {},
            diagnosis_name: '',
            diagnoses: [],
            count_diagnoses: 0,
            count_founded_diagnoses: 0,
            isOpen: false,
            registry_diagnoses: [],
            removed_registry_diagnoses: [],
            isJSONValid: true,
            JSONerr: '',
        }
    },
    async asyncData({ params }) {
        return {
            id: params.id,
        }
    },
    head() {
        return {
            title: "Изменение региста " + this.name,
        }
    },
    methods: {
        async getRegistryDiagnoses() {
            try {
                let registry = await this.$axios.get(`/api/v1/diagnosis_registry/${this.id}`);
                this.id = registry.data.result.id;
                this.short_name = registry.data.result.short_name;
                this.name = registry.data.result.name;
                try {
                    this.medical_record_transcript_settings = JSON.stringify(registry.data.result.medical_record_transcript_settings, null, 2);
                } catch (err) {
                    this.medical_record_transcript_settings = ""
                }
                let response = await this.$axios.get(`/api/v1/diagnosis_registry/${this.id}/diagnoses`);
                this.registry_diagnoses = response.data.result;
                this.count_diagnoses = response.data.retExtInfo.count_items;
                console.log(JSON.parse(registry.data.result.medical_record_transcript_settings));
                console.log(this.medical_record_transcript_settings);
            } catch ({ response }) {
                console.log(response);
            }
        },
        async onChange() {
            try {
                let response = await this.$axios.get(`/api/v1/ref_inf/diagnosis?q=${this.diagnosis_name}`);
                this.diagnoses = response.data.result;
                this.count_founded_diagnoses = response.data.retExtInfo.count_items;
                this.isOpen = true;
            } catch ({ response }) {
                console.log(response);
            }
        },
        setResult(mkb_code, name) {
            this.isOpen = false;
            this.diagnosis_name = '';
            this.count_diagnoses += 1;
            this.registry_diagnoses.push({ "id": 0, "registry": this.id, "registry_name": this.short_name, "diagnosis": mkb_code, "diagnosis_name": name });
        },
        removeItem(index) {
            this.count_diagnoses -= 1;
            this.removed_registry_diagnoses.push(this.registry_diagnoses.splice(index, 1)[0]);
        },
        handleClickOutside(event) {
            if (!this.$el.contains(event.target)) {
                this.isOpen = false;
                this.diagnosis_name = '';
            }
        },
        onJSONChange() {
            let jsonValue = "";
            try {
                jsonValue = JSON.parse(this.medical_record_transcript_settings);
                this.JSONerr = '';
                this.isJSONValid = true
            } catch (err) {
                this.JSONerr = JSON.stringify(err.message);
                this.isJSONValid = false
            }
        },
        async registryUpdate() {
            this.isOpen = false;
            try {
                let response = await this.$axios.put(`/api/v1/diagnosis_registry/${this.id}`, { "short_name": this.short_name, "name": this.name, "medical_record_transcript_settings": JSON.parse(this.medical_record_transcript_settings) });
                console.log(response);
                for (let i = 0; i < this.removed_registry_diagnoses.length; i += 1) {
                    if (this.removed_registry_diagnoses[i].id != 0) {
                        let response = await this.$axios.delete(`/api/v1/diagnosis_registry_item/${this.removed_registry_diagnoses[i].id}`);
                    }
                }
                for (let i = 0; i < this.registry_diagnoses.length; i += 1) {
                    if (this.registry_diagnoses[i].id == 0) {
                        let response = await this.$axios.post(`/api/v1/diagnosis_registry_item`, { "registry": this.id, "diagnosis": this.registry_diagnoses[i].diagnosis });
                    }
                }
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
        document.addEventListener('click', this.handleClickOutside);
    },
    destroyed() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    computed: {
        isComplete() {
            return !this.$v.$invalid && this.count_diagnoses != 0 && this.isJSONValid;
        },
        // prettyFormat() {
        //     this.jsonerror = "";
        //     let jsonValue = "";
        //     try {
        //         jsonValue = JSON.parse(this.medical_record_transcript_settings)
        //     }
        //     catch (e) {
        //         this.jsonerror = JSON.stringify(e.message)
        //         var textarea = this.$refs.medical_record_transcript_settings
        //         if (this.jsonerror.indexOf('position') > -1) {
        //             var positionStr = this.jsonerror.lastIndexOf('position') + 8;
        //             var posi = parseInt(this.jsonerror.substring(positionStr, this.jsonerror.lastIndexOf('"')));
        //             if (posi >= 0) {
        //                 textarea.setSelectionRange(posi, posi + 1);
        //             }
        //         }
        //         return "";
        //     }
        //     return JSON.stringify(jsonValue, null, 2);
        // },
    },
    validations: {
        short_name: {
            required,
            maxLength: maxLength(25)
        },
        name: {
            required,
            maxLength: maxLength(125)
        },
    },
}
</script>

<style type="text/css">
.fld-error-all {
    display: block;
    color: #dc3545;
}

.fld-error .msg-error .msg-error-j {
    display: block;
    color: #dc3545;
}

.msg-error {
    display: none;
}
</style>