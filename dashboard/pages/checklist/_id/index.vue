<template>
  <div class="wrapper mt-3">
    <div class="animated fadeIn">
        <h5>{{checklist.name}}
        <span class="float-right clearfix"><i class="fa fa-plus-square fa-lg mt-4"></i> New Question</span> 
        </h5>
        <p class="lead">{{checklist.description}}</p>
        <hr/>
        <b-list-group flush>

            <b-list-group-item
            v-for="question in questions"
            :key="question.id"
            >
                {{question.question}}
                <span>
                    <a :href="question.get_admin_change_url"><i class="fa fa-edit fa-sm ml-2 text-success"></i></a>  
                    <i class="fa fa-times fa-sm ml-2 text-danger"></i>
                </span>
                <div v-if="question.children.length > 0">
                    <div v-if="question.groups.length === 0">
                        <b-card-text 
                        v-for="child in question.children"
                        :key="child.id"
                        class="pl-3"
                        >
                        {{child.question}}
                        <span>
                            <a :href="child.get_admin_change_url"><i class="fa fa-edit fa-sm ml-2 text-success"></i></a>                            
                            <i class="fa fa-times fa-sm ml-2 text-danger"></i>
                        </span>
                        </b-card-text>
                    </div>
                    <div v-else>    
                        <div v-for="group in groupChildren({ 'children': question.children, 'groups': question.groups })" :key="group.id">
                            <h6>
                                {{group.name}}
                                <span>
                                    <i class="fa fa-edit fa-sm ml-2 text-success"></i>
                                    <i class="fa fa-times fa-sm ml-2 text-danger"></i>
                                </span>
                            </h6>
                            <b-card-text 
                            v-for="child in group.questions"
                            :key="child.id"
                            class="pl-3">
                            {{child.question}}
                            <span>
                                <a :href="child.get_admin_change_url"><i class="fa fa-edit fa-sm ml-2 text-success"></i></a>  
                                <i class="fa fa-times fa-sm ml-2 text-danger"></i>
                            </span>
                            </b-card-text>
                        </div>  
                    </div>               
                </div>
                <div v-else>
                  <!--  Has no children -->
                </div>
            
            </b-list-group-item>

        </b-list-group>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
        checklist : {},
        questions: [],
    }
  },
  methods: {
      getChecklist(){  
        // Get Questions
        this.$axios.$get('checklist/questions/all?checklist_id=' + this.$route.params.id , { headers: ""})
        .then(res => {
            if(res.length > 0){
                // Get Checklist Details
                this.checklist = res[0].checklist
                // Assign Questions
                this.questions = res.map(question => {
                    return question
                })
            }
        })  
      },
      groupChildren(data) {
          var groups = data.groups
          groups.map(group => group.questions = [])
          data.children.map( child => {
              groups.map(group => {
                  if(child.group.id === group.id){
                      group.questions.push(child)
                  }
              })              
          })
          return groups
      }
  },
  mounted() {
      this.getChecklist()
  }
}
</script>

</style>
