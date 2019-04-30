<template>
  <v-app dark>
    <v-navigation-drawer
      :mini-variant.sync="miniVariant"
      :clipped="clipped"
      v-model="drawer"
      fixed
      app
    >
      <v-list>
        <v-list-tile router :to="item.to" :key="i" v-for="(item, i) in items" exact>
          <v-list-tile-action>
            <v-icon v-html="item.icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar fixed app :clipped-left="clipped">
      <!-- <v-toolbar-side-icon @click="drawer = !drawer"></v-toolbar-side-icon> -->
      <!-- <v-btn
        icon
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon v-html="miniVariant ? 'chevron_right' : 'chevron_left'"></v-icon>
      </v-btn>
      <v-btn
        icon
        @click.stop="clipped = !clipped"
      >
        <v-icon>web</v-icon>
      </v-btn>
      <v-btn
        icon
        @click.stop="fixed = !fixed"
      >
        <v-icon>remove</v-icon>
      </v-btn>-->
      <v-toolbar-title v-text="title" ></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn class="mx-3 mt-5"  fab bottom right icon color="blue" @click.stop="save">
        <v-icon>backup</v-icon>
      </v-btn>
      <v-btn class="mx-3 mt-5 pl-5"  fab bottom right icon color="green" @click.stop="load">
        <v-icon>launcher</v-icon>
      </v-btn>
      <v-btn class="mx-3 mt-5"  fab bottom right icon color="pink" @click.stop="refresh">
        <v-icon>cached</v-icon>
      </v-btn>
    </v-toolbar>
    <v-content >
    <SnackBar :text="snackBarText" :snackbar="openSnackBar" @close="openSnackBar=false"/>

      <v-container class="pb-1 pt-3">
        <nuxt/>
      </v-container>
    </v-content>
    <!-- <v-navigation-drawer
      temporary
      :right="right"
      v-model="rightDrawer"
      fixed
      class="hidden-lg-and-down"
    >
      <v-list>
        <v-list-tile @click.native="right = !right">
          <v-list-tile-action>
            <v-icon light>compare_arrows</v-icon>
          </v-list-tile-action>
          <v-list-tile-title>Switch drawer (click me)</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer> -->
    <v-footer :fixed="fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import SnackBar from "../components/SnackBar"
export default {
  data() {
    return {
      snackBarText:'loren',
      openSnackBar:false,
      clipped: false,
      drawer: true,
      fixed: true,
      items: [
        { icon: "apps", title: "Welcome", to: "/" },
        { icon: "bubble_chart", title: "RBD", to: "/rbd_main" },
        // { icon: "settings", title: "Settings", to: "/Settings" },
        { icon: "help", title: "Guide", to: "/FAQ" },
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: "AvailabiliCalc"
    };
  },
  mounted: function(){
    console.log(this.$router)
  },
  components:{
    SnackBar
  },
  
  methods: {
    refresh: function() {
      document.location.reload();
    },
    save: async function () {
      eel.save()((result) =>{if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }}  )
      
      
    },
    load: async function () {
      eel.load()((result) => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }} )
      this.$router.push('/rbd_main')
    }
  }
};
</script>
