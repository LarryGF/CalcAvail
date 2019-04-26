<template>
  <v-layout column justify-center align-center>
    <v-flex xs10 >
      <div class="text-xs-center">
        <h1>General</h1>
        <v-card v-for="card in cardsGeneral" :key="card.key" light width="1000" class="mb-4">
          <v-toolbar card :color="card.color" dark @click="hide(card)">
            <v-toolbar-title ><v-icon>{{card.icon}}</v-icon> {{card.title}}</v-toolbar-title>
              <v-spacer></v-spacer>
            <v-toolbar-items>
              <v-btn icon @click="hide(card)"><v-icon>{{card.icon2}}</v-icon></v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <v-card-text class="subheading" v-if="card.show">{{card.text}}</v-card-text>
        </v-card>
        <h1>RBD</h1>
        <v-card v-for="card in cardsRbd" :key="card.key" light width="1000" class="mb-4">
          <v-toolbar card :color="card.color" dark @click="hide(card)">
            <v-toolbar-title ><v-icon>{{card.icon}}</v-icon> {{card.title}}</v-toolbar-title>
              <v-spacer></v-spacer>
            <v-toolbar-items>
              <v-btn icon @click="hide(card)"><v-icon>{{card.icon2}}</v-icon></v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <v-card-text class="subheading" v-if="card.show">{{card.text}}</v-card-text>
        </v-card>
      </div>

    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data: function() {
    return {
      cardsRbd:[
        {
          key:0,
          title:'Creating a new RBD',
          color:'blue-grey darken-1',
          text:"To create a new RBD you just have to click on the 'Start' button on the welcome page, or go directly \
          into the 'RBD' button in the navigation drawer. The 'RBD' button is also a good way to go back to the RBD view\
          in case your in another view.",
          icon:'add_circle',
          icon2:'expand_more',
          show:false

        },
        {
          key:1,
          title:'Adding blocks to an RBD',
          color:'blue-grey darken-3',
          text:"After you click on the 'Add block' button, a dialog will pop up. You will have the choice of either creating\
          a single block, or creating several blocks in parallel. If you choose to create the parallel group, you'll have to\
          specify how many of those blocks are needed to stay active at the same time for the system to work. You can fill the \
          forms by clicking on the input spaces and selecting the choice you want, or you can start typing and the software will\
          suggest you the right choices. By tapping the 'Enter' key, it will autosubmit your choice and skip to the next one\
          if all your choices are accurate, pressing the 'Enter' key will also submit your information.",
          icon2:'expand_more',
          icon:'add_circle',
          show:false

        },
        {
          key:2,
          title:'Adding a path between two RBD blocks',
          color:'blue-grey darken-1',
          text:"Adding a path is a similar process to creating a new Block. You just have to click the 'Add path' button\
          and type or select the source block and the target block. Much like adding blocks, by tapping the 'Enter' key\
          you can confirm your selection.",
          icon:'add_circle',
          icon2:'expand_more',
          show:false

        },
        {
          key:2,
          title:'Adding a path between two RBD blocks',
          color:'blue-grey darken-3',
          text:"Adding a path is a similar process to creating a new Block. You just have to click the 'Add path' button\
          and type or select the source block and the target block. Much like adding blocks, by tapping the 'Enter' key\
          you can confirm your selection.",
          icon:'add_circle',
          icon2:'expand_more',
          show:false

        },
        {
          key:3,
          title:'Delete a block or path',
          color:'blue-grey darken-1',
          text:"Similar to the previous procedures, deleting a block or path is fairly simple, just pick the desired blcok \
          or path and click the 'Delete' button or the 'Enter' key.",
          icon:'delete', 
          icon2:'expand_more',
          show:false

        },
        {
          key:4,
          title:'Attach a Markov Chain to a block',
          color:'blue-grey darken-3',
          text:"The 'Attach chain' button creates a new Markov Chain and binds it to a specific block, said Markov Chain \
          will be the responsible of obtaining the block's availability. As soon as you select to which block you wanna append\
          the Markov Chain, the software will take you to a new view where you can interact with the newly created CTMC. If you\
          wanna return to the main RBD view you just have to click in the 'RBD' button in the navigation drawer. Double clicking \
          any block will take you to it's CTMC view",
          icon:'attach_file', 
          icon2:'expand_more',
          show:false

        },
      ],
      cardsGeneral:[
        {
          key:0,
          title:'Saving and loading',
          color:'blue-grey darken-1',
          text:"In the 'Settings' tab you will find the option to Save and Load your project. It saves the entire project \
          in a file located in the project's root folder called 'save.json'.",
          icon:'backup', 
          icon2:'expand_more',
          show:false

        },
        {
          key:1,
          title:'Refresh the view',
          color:'blue-grey darken-3',
          text:"Since most elements are arranged automatically in the screen it might happen that you encounter some visualization\
          issues, some elements being positioned on top of each other and such. For that reason there's a pink floating action button\
          on the top right corner of the screen, clicking it will refresh the view and force the page to re render and the components will\
          be rearranged. You could also press the 'F5' key, whatever is easier.",
          icon:'refresh', 
          icon2:'expand_more',
          show:false

        },
      ]
    };
  },

  methods: {
    hide: function(card){
      
      card.show = !card.show
      card.icon2 = (card.icon2 == 'expand_more') ? 'expand_less': 'expand_more'
    }
  }
};
</script>

