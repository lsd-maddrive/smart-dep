<template>
  <v-container fluid>
    <h1 class="text-center">Новые устройства</h1>
    <v-row justify="center">
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
                <v-card>
                  <v-card-title>
                    <span class="headline">Обновление устройства</span>
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
                            <v-select
                              v-model="deviceEditItem.type_id"
                              :rules="[v => !!v || 'Тип обязателен']"
                              :items="deviceTypes"
                              item-text="desc"
                              item-value="id"
                              label="Тип"
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="6" md="6">
                            <v-select
                              v-model="deviceEditItem.place_id"
                              :rules="[v => !!v || 'Помещение обязательно']"
                              :items="places"
                              item-text="num"
                              item-value="id"
                              label="Помещение"
                            ></v-select>
                          </v-col>
                        </v-row>
                      </v-form>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="closeEdit"
                      :disabled="loading.deviceSave"
                    >Отмена</v-btn>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="saveDevice"
                      :loading="loading.deviceSave"
                    >Сохранить</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon small v-on="on" class="mr-2" @click="pingDevice(item)">mdi-alarm-light</v-icon>
              </template>
              <span>Пинг</span>
            </v-tooltip>

            <v-icon small class="mr-2" @click="editDevice(item)">mdi-pencil</v-icon>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon small v-on="on" @click="deleteDevice(item)">mdi-delete</v-icon>
              </template>
              <span>Удалить</span>
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
      loading: {
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
        { text: "Дата добавления", value: "date" },
        { text: "IP адрес", value: "ip_addr" },
        { text: "Действия", value: "actions", sortable: false }
      ],
      devices: [],
      places: [],
      deviceTypes: []
    };
  },
  computed: {
    editMode() {
      return this.$route.params.id ? true : false;
    }
  },
  components: {},
  methods: {
    typeDesc: item => item.desc,
    itemId: item => item.id,
    placeNum: item => item.num,
    /**
     * Table dependent methods
     */
    editDevice(item) {
      this.deviceEditItem = Object.assign({}, item);
      this.deviceEditDialogue = true;
    },
    pingDevice(item) {
      Services.pingDevice(item).then(
        resp => {
          this.$toasted.success("Пинг успешно отправлен");
        },
        err => {
          this.$toasted.success("Не удалось отправить пинг: " + err);
        }
      );
    },

    deleteDevice(item) {
      // const index = this.desserts.indexOf(item);
      let result = confirm(
        `Вы уверены, что хотите удалить устройство ${item.id}?`
      );
      if (result) {
        this.$toasted.info("Удаление устройства");
        const device = Object.assign({}, item);
        Services.deleteDevice(device).then(
          resp => {
            this._updateDevices();
            this.$toasted.success("Устройство успешно удалено!");
          },
          error => {
            this.$toasted.error("Не удалось удалить устройство");
          }
        );
      }
    },
    closeEdit() {
      this.deviceEditDialogue = false;
    },

    saveDevice() {
      let validationResult = this.$refs.deviceForm.validate();
      if (!validationResult) {
        return;
      }

      let device = this.deviceEditItem;
      this.loading.deviceSave = true;

      let currentType = this.deviceTypes.find(x => x.id == device.type_id);
      device.type = currentType.name;
      device.config = currentType.default_config;

      Services.updateDevice(device).then(
        () => {
          this._updateDevices();
          this.$toasted.success("Устройство успешно обновлено!");
          this.loading.deviceSave = false;
          this.closeEdit();
        },
        error => {
          this.$toasted.error("Не удалось обновить устройство");
          this.loading.deviceSave = false;
        }
      );
    },
    _updateDevices() {
      this.devices = [];
      this.loading.table = true;
      Services.getNewDevices().then(
        resp => {
          this.loading.table = false;
          for (var dev of resp.data) {
            this.devices.push({
              id: dev.id,
              ip_addr: dev.ip_addr,
              date: new Date(dev.reg_ts * 1000)
            });
          }
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
    this._updateDevices();
    this.$store
      .dispatch("syncPlaces")
      .then(resp => {
        this.places = resp;
      })
      .catch(err => {
        this.$toasted.error("Не удалось обновить комнаты =(");
      });
    this.$store
      .dispatch("syncDeviceTypes")
      .then(resp => {
        this.deviceTypes = resp;
      })
      .catch(err => {
        this.$toasted.error("Не удалось обновить типы контроллеров =(");
      });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
