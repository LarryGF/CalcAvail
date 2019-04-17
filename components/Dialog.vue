<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px" dark>
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        <v-card-title>
          <span class="headline">Define a rate for this transition</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid>
            <!-- <v-layout > -->
            <!-- <v-flex xs12 sm6 md4> -->
            <v-text-field
              v-model="value"
              label="Transition rate"
              required
              :rules="[rules.required]"
              counter
              maxlength="5"
              loading
            >
            <v-progress-linear slot="progress" :value="progress" :color="color" height="7"></v-progress-linear>
            </v-text-field>
            <!-- </v-flex > -->
            <!-- <v-flex xs12 sm6 md4>
                <v-text-field label="Legal middle name" hint="example of helper text only on focus"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field
                  label="Legal last name*"
                  hint="example of persistent helper text"
                  persistent-hint
                  required
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Email*" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Password*" type="password" required></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-select
                  :items="['0-17', '18-29', '30-54', '54+']"
                  label="Age*"
                  required
                ></v-select>
            </v-flex>-->
            <!-- <v-flex xs12 sm6>
                <v-autocomplete
                  :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']"
                  label="Interests"
                  multiple
                ></v-autocomplete>
            </v-flex>-->
            <!-- </v-layout> -->
          </v-container>
          <!-- <small>*indicates required field</small> -->
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="$emit('save',value)">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: 'Dialog',
  props: {
    dialog: Boolean
  },
  data: () => ({
    value: '',
    custom: true,
    rules: {
      required: value => !!value || 'Required'
    }
  }),
  computed: {
    progress () {
      return Math.min(100, this.value.length * 20)
    },
    color () {
      return ['error', 'warning', 'success'][Math.floor(this.progress / 40)]
    }
  }
}
</script>