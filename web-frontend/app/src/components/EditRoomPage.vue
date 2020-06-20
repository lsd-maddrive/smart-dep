<template>
  <v-container fluid>
    <h1 class="text-center" v-if="editMode">Редактирование комнаты</h1>
    <h1 class="text-center" v-else>Создание комнаты</h1>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="8">
        <v-form ref="placeForm">
          <v-text-field
            label="Название"
            v-model.trim="place.name"
            :rules="nameRules"
            name="login"
            type="text"
            required
          ></v-text-field>

          <v-text-field
            label="Номер комнаты"
            v-model.trim="place.num"
            :rules="numRules"
            name="login"
            type="text"
            required
          ></v-text-field>

          <v-row>
            <v-col cols="6" sm="6" md="6">
              <v-switch v-model="place.attr_projector" class="mx-2" label="Проектор"></v-switch>
            </v-col>
            <v-col cols="6" sm="6" md="6">
              <v-switch v-model="place.attr_board" class="mx-2" label="Доска"></v-switch>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" sm="6" md="6">
              <v-text-field
                label="Вместимость"
                v-model="place.attr_people"
                :rules="[v => !!v || 'Количество обязательно']"
                type="number"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="6" sm="6" md="6">
              <v-text-field
                label="Компьютеры"
                v-model="place.attr_computers"
                :rules="[v => !!v || 'Количество обязательно']"
                type="number"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" sm="6" md="6">
              <v-select
                v-model="place.attr_os"
                :rules="[v => !!v || 'ОС обязательна']"
                :items="operating_systems"
                item-text="desc"
                item-value="id"
                small-chips
                attach
                multiple
                label="ОС"
              ></v-select>
            </v-col>
            <v-col cols="6" sm="6" md="6">
              <v-select
                v-model="place.attr_software"
                :rules="[v => !!v || 'ПО обязательно']"
                :items="software"
                item-text="desc"
                item-value="id"
                small-chips
                attach
                multiple
                label="ПО"
              ></v-select>
            </v-col>
          </v-row>
          <v-row v-if="editMode" justify="center">
            <v-col cols="6" sm="6" md="6">
              <v-file-input
                accept="image/*"
                label="Изображение"
                show-size
                dense
                prepend-icon="mdi-file-image-outline"
                :rules="imageRules"
                v-model="placeImage"
              ></v-file-input>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-spacer></v-spacer>
            <v-btn
              v-if="!editMode"
              color="blue darken-1"
              @click="createSubmit"
              :loading="loading.createUpdate"
              text
            >Создать</v-btn>
            <v-btn
              v-if="editMode"
              color="blue darken-1"
              @click="updateSubmit"
              :loading="loading.createUpdate"
              text
            >Сохранить</v-btn>
            <v-btn
              v-if="editMode"
              color="red darken-1"
              @click="deleteSubmit"
              :loading="loading.delete"
              text
            >Удалить</v-btn>
            <v-btn color="gray darken-1" @click="cancelSubmit" text>Отмена</v-btn>
          </v-row>
        </v-form>
      </v-col>
    </v-row>

    <v-row justify="center" v-if="editMode">
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="devices"
          item-key="name"
          :loading="loading.table"
          loading-text="Загружаю устройства"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title>Устройства</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="deviceEditDialogue" max-width="500px">
                <!-- <template v-slot:activator="{ on }">
                    <v-btn color="primary" dark class="mb-2" @click="addDevice" v-on="on">Добавить</v-btn>
                </template>-->
                <v-card>
                  <v-card-title>
                    <span class="headline">{{ deviceEditTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-form ref="deviceForm">
                        <v-row>
                          <v-col cols="12" sm="6" md="6">
                            <v-text-field
                              :rules="[v => !!v || 'Наименование обязательно']"
                              v-model="deviceEditItem.name"
                              label="Наименование"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="6" v-if="deviceEditItem.id">
                            <v-text-field v-model="deviceEditItem.id" label="ID" readonly></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-combobox
                              v-model="deviceEditItem.icon_name"
                              :prepend-inner-icon="deviceEditItem.icon_name"
                              :items="icons"
                              :rules="[v => !!!v || /^mdi-/.test(v) || 'Невалидная иконка' ]"
                              label="Иконка"
                            >
                              <template slot="item" slot-scope="data">
                                <span>
                                  <v-icon>{{ data.item }}</v-icon>
                                  {{ data.item }}
                                </span>
                              </template>
                            </v-combobox>
                          </v-col>
                          <!-- <v-col cols="12" sm="6" md="6">
                              <v-select
                                v-model="deviceEditItem.type"
                                :rules="[v => !!v || 'Тип обязателен']"
                                :items="deviceTypes"
                                :item-text="typeDesc"
                                :item-value="itemId"
                                label="Тип"
                              ></v-select>
                          </v-col>-->
                          <!-- <v-col cols="12" sm="6" md="6">
                              <v-select
                                disabled
                                v-model="deviceEditItem.place_id"
                                :rules="[v => !!v || 'Помещение обязательно']"
                                :items="places"
                                :item-text="placeNum"
                                :item-value="itemId"
                                label="Помещение"
                              ></v-select>
                          </v-col>-->
                        </v-row>
                      </v-form>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="close"
                      :disabled="loading.deviceSave"
                    >Отмена</v-btn>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="save"
                      :loading="loading.deviceSave"
                    >Сохранить</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="editDevice(item)">mdi-pencil</v-icon>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on" small @click="resetDevice(item)">mdi-undo</v-icon>
              </template>
              <span>Сброс</span>
            </v-tooltip>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import RoomDevicesTable from "@/components/RoomDevicesTable";
import Services from "@/services/Services";

export default {
  name: "RoomEditorCreator",
  data() {
    return {
      // Default data
      place: {
        attr_people: 25,
        attr_computers: 10,
        attr_os: ["windows"],
        attr_software: [],
        attr_board: true,
        attr_projector: false
      },
      placeImage: null,
      imageRules: [
        value =>
          !value ||
          value.size < 2000000 ||
          "Изображение должно быть не более 2 МБ",
        value =>
         !value ||
         value.type.startsWith('image/') || "Невалидный тип"
      ],
      loading: {
        createUpdate: false,
        delete: false,
        table: false,
        deviceSave: false
      },
      nameRules: [v => !!v || "Название обязательно"],
      numRules: [v => !!v || "Номер обязателен"],

      // Table data
      deviceEditDialogue: false,
      deviceEditItem: {},
      headers: [
        {
          text: "ID",
          align: "start",
          sortable: false,
          value: "id"
        },
        { text: "Наименование", value: "name" },
        { text: "Последняя активность", value: "last_active_date" },
        { text: "Тип", value: "type" },
        { text: "Действия", value: "actions", sortable: false }
      ],
      devices: [],
      deviceTypes: [],
      places: [],
      operating_systems: [
        {
          desc: "Linux",
          id: "linux"
        },
        {
          desc: "Windows",
          id: "windows"
        },
        {
          desc: "MacOS",
          id: "mac"
        }
      ],
      software: [
        {
          desc: "MATLAB",
          id: "matlab"
        },
        {
          desc: "MPLabX",
          id: "mplabx"
        },
        {
          desc: "LabView",
          id: "labview"
        }
      ],
      icons: Services.getIcons()
    };
  },
  computed: {
    editMode() {
      return this.$route.params.id ? true : false;
    },
    placeId() {
      return this.$route.params.id;
    },

    isNewDevice() {
      return typeof this.deviceEditItem.id === "undefined";
    },
    deviceEditTitle() {
      return this.deviceEditItem.id
        ? "Редактировать устройство"
        : "Добавить устройство";
    }
  },
  components: {
    "devices-table": RoomDevicesTable
  },
  methods: {
    cancelSubmit: function() {
      this.$router.push(this.$route.query.returnUrl || { name: "Home" });
    },
    createSubmit: function() {
      let validationResult = this.$refs.placeForm.validate();
      if (!validationResult) {
        return;
      }

      this.loading.createUpdate = true;
      Services.createPlace(this.place).then(
        resp => {
          this.$toasted.success("Помещение успешно создано!");
          this.$router.push({ name: "Home" });
        },
        error => {
          this.$toasted.error("Создание помещения не удалось");
          this.loading.createUpdate = false;
        }
      );
    },
    updateSubmit: function() {
      let validationResult = this.$refs.placeForm.validate();
      if (!validationResult) {
        return;
      }

      this.loading.createUpdate = true;
      Services.updatePlace(this.place).then(
        resp => {
          if (this.placeImage) {
            var formData = new FormData();
            formData.append("image", this.placeImage);

            Services.sendPlaceImage(this.place, formData).then(
              resp => {
                this.$toasted.success("Помещение успешно обновлено!");
                this.$router.push({ name: "Home" });
              },
              err => {
                this.$toasted.error("Загрузка изображения не удалась");
                this.loading.createUpdate = false;
              }
            );
          } else {
            this.$toasted.success("Помещение успешно обновлено!");
            this.$router.push({ name: "Home" });
          }
        },
        error => {
          this.$toasted.error("Создание помещения не удалось");
          this.loading.createUpdate = false;
        }
      );
    },
    deleteSubmit: function() {
      let result = confirm(
        `Вы уверены, что хотите удалить помещение ${this.sourcePlace.num}?`
      );
      if (!result) {
        return;
      }

      this.loading.delete = true;
      Services.deletePlace(this.sourcePlace).then(
        resp => {
          this.$toasted.success("Помещение успешно удалено!");
          this.$router.push({ name: "Home" });
        },
        error => {
          this.$toasted.error("Удаление помещения не удалось");
          this.loading.delete = false;
        }
      );
    },
    /**
     * Table dependent methods
     */
    addDevice() {
      this.deviceEditItem = {
        place: this.sourcePlace.num
      };
      this.deviceEditDialogue = true;
    },
    editDevice(item) {
      this.deviceEditItem = Object.assign({}, item);
      this.deviceEditDialogue = true;
    },

    resetDevice(item) {
      // const index = this.desserts.indexOf(item);
      let result = confirm(
        `Вы уверены, что хотите удалить устройство ${item.id}?`
      );
      if (result) {
        this.$toasted.info("Сброс устройства");
        const device = Object.assign({}, item);
        Services.resetDevice(device).then(
          resp => {
            this._updateDevices();
            this.$toasted.success("Устройство успешно сброшено!");
          },
          error => {
            this.$toasted.error("Не удалось удалить устройство");
          }
        );
      }
    },
    close() {
      this.deviceEditDialogue = false;
    },

    save() {
      let validationResult = this.$refs.deviceForm.validate();
      if (!validationResult) {
        return;
      }

      const device = this.deviceEditItem;
      this.loading.deviceSave = true;

      if (this.isNewDevice) {
        Services.createDevice(device).then(
          () => {
            this._updateDevices();
            this.$toasted.success("Устройство успешно добавлено!");
            this.loading.deviceSave = false;
            this.close();
          },
          error => {
            this.$toasted.error("Не удалось добавить устройство");
            this.loading.deviceSave = false;
          }
        );
      } else {
        Services.updateDevice(device).then(
          () => {
            this._updateDevices();
            this.$toasted.success("Устройство успешно обновлено!");
            this.loading.deviceSave = false;
            this.close();
          },
          error => {
            this.$toasted.error("Не удалось обновить устройство");
            this.loading.deviceSave = false;
          }
        );
      }
    },
    _updateDevices() {
      this.devices = [];
      const placeId = this.$route.params.id;
      this.loading.table = true;
      Services.getPlaceDevices({ id: placeId }).then(
        resp => {
          this.loading.table = false;
          this.devices = resp.data.map(function(x) {
            x.last_active_date = new Date(x.last_ts * 1000);
            return x;
          });
        },
        err => {
          this.loading.table = false;
          this.$toasted.error("Не удалось получить список устройств");
        }
      );
    }
  },
  components: {},
  created() {
    this.$store
      .dispatch("syncDeviceTypes")
      .then(resp => {
        this.deviceTypes = resp;
      })
      .catch(err => {
        this.$toasted.error("Не удалось обновить типы контроллеров =(");
      });
    this.$store
      .dispatch("syncPlaces")
      .then(resp => {
        this.places = resp;
      })
      .catch(err => {
        this.$toasted.error("Не удалось обновить комнаты =(");
      });

    const placeId = this.$route.params.id;
    if (placeId) {
      this.$store.dispatch("validatePlace", { placeId: placeId }).then(
        resp => {
          // Copy to have external data copy
          this.sourcePlace = Object.assign({}, resp);
          this.place = Object.assign({}, resp);

          // Update list of devices
          this._updateDevices();
        },
        err => {
          this.$toasted.error("Комната " + this.placeId + " не найдена =(");
          this.$router.push({ name: "Home" });
        }
      );
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
