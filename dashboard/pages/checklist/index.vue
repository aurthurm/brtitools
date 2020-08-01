<template>
  <div class="wrapper">
    <div class="animated fadeIn">
      <a class="" @click="showSectionModal($event, {new: true})"><i class="fa fa-plus-square fa-lg mt-4"></i> New Section</a>
      <a class="ml-3" @click="showChecklistModal($event, {new: true})"><i class="fa fa-plus-square fa-lg mt-4"></i> New CheckList</a>
      <hr />
      <b-row>

        <b-col 
        v-for="section in checklists" 
        :key="section.id"
        md="6" >
          <b-card
            header-tag="header"
            footer-tag="footer">
            <div slot="header">
              <i class="fa fa-align-justify"></i> <strong>{{section.name}}</strong><small></small>
            </div>
            <b-list-group>

              <b-list-group-item 
              v-for="checklist in section.checklists"
              :key="checklist.id"
              :href="'checklist/' + checklist.id" class="flex-column align-items-start p-2">
                <div class="d-flex w-100 justify-content-between">
                  <h5 class="mb-1">{{checklist.name}}</h5>
                </div>
                <p class="mb-1">
                  {{checklist.description}}
                </p>
              </b-list-group-item>

            </b-list-group>
          </b-card>
        </b-col>

      </b-row>
    </div>

    <!-- Section Modal -->
    <b-modal 
    ref="sectionModal"
    title="New Section" 
    centered 
    @ok="handleSectionOk"
    >
      <b-form ref="form">
          <b-row>
              <b-col>
                  <b-form-group
                  id="fieldset-horizontal"
                  label-cols-sm="4"
                  label-cols-lg="3"
                  label-size="sm"
                  description=""
                  label="Section Name"
                  label-for="sectionName"
                  invalid-feedback="name is required"
                  >
                      <b-form-input 
                      id="sectionName"
                      v-model="section.name"
                      required
                      ></b-form-input>
                  </b-form-group>
              </b-col>                
          </b-row>        
          <b-row>
              <b-col>
                  <b-form-group
                  id="fieldset-horizontal"
                  label-cols-sm="4"
                  label-cols-lg="3"
                  label-size="sm"
                  label="Description:"
                  label-for="description"
                  >
                      <b-form-textarea 
                      id="description"
                      ref="description"
                      v-model="section.description"
                      size="sm"
                      >
                      </b-form-textarea>
                  </b-form-group>
              </b-col>
          </b-row>
      </b-form>
    </b-modal>

    <!-- Checklist Modal -->
    <b-modal 
    ref="checklistModal"
    title="New Checklist" 
    centered 
    @ok="handleChecklistOk"
    >
      <b-form ref="form" >
          <b-row>
              <b-col>
                  <b-form-group
                  id="fieldset-horizontal"
                  label-cols-sm="4"
                  label-cols-lg="3"
                  label-size="sm"
                  description=""
                  label="Name"
                  label-for="checklistName"
                  invalid-feedback="name is required"
                  >
                      <b-form-input 
                      id="checklistName"
                      v-model="checklist.name"
                      required
                      ></b-form-input>
                  </b-form-group>
              </b-col>                
          </b-row>        
          <b-row>
              <b-col>
                  <b-form-group
                  id="fieldset-horizontal"
                  label-cols-sm="4"
                  label-cols-lg="3"
                  label-size="sm"
                  label="Description:"
                  label-for="description"
                  >
                      <b-form-textarea 
                      id="description"
                      ref="description"
                      v-model="checklist.description"
                      size="sm"
                      >
                      </b-form-textarea>
                  </b-form-group>
              </b-col>
          </b-row>
          <b-row>
              <b-col>
                  <b-form-group
                  id="fieldset-horizontal"
                  label-cols-sm="4"
                  label-cols-lg="3"
                  label-size="sm"
                  label="Section:"
                  label-for="section"
                  >
                      <b-form-select 
                      id="section"
                      ref="section"
                      size="sm"
                      v-model="checklist.sectionId"
                      :options="options.sections.options"
                      >
                      </b-form-select>
                  </b-form-group>
              </b-col>
          </b-row>   
      </b-form>
    </b-modal>


  </div>
</template>

<script>

export default {
  data() {
    return {
      newSection: true,
      section: {
        id: null,
        name: "",
        description: "",
      },
      sections: [],
      newChecklist: true,
      checklist: {
        id: null,
        name: "",
        description: "",
        sectionId: null,
      },
      checklists: [],
      options: {                
          sections : {
              options: [
                  { value: null, text: "Select a Section" }
              ]
          }
      }
    }
  },
  methods:{
    showSectionModal(event, data) {
      this.newSection = data.new
      if (this.newSection){
        this.section.id = null
        this.section.name = ""
        this.section.description = ""
      } else {

      }
      this.$refs['sectionModal'].show()
    },
    handleSectionOk(bvModalEvt){
        bvModalEvt.preventDefault();
        this.handleSectionSubmit()            
    },
    handleSectionSubmit(){
        let axiosMethod = this.newSection ? this.$axios.$post : this.$axios.$put
        axiosMethod('checklist/section/add', this.section, { headers: ""})
        .then(res => {
          this.$refs['sectionModal'].hide()
          this.checklists.push(res)
        })
        .catch(err => console.log(err))
    },
    initSections() {
        // Initialise Sections           
        this.options.sections.options = [{ value: null, text: "Select a City"}]  
        this.$axios.$get('checklist/section/all', { headers: ""})
        .then(res => {
            res.forEach(section => {
                this.options.sections.options.push({ value: section.id, text: section.name})
            });
        })
    },
    showChecklistModal(event, data) {
      this.newChecklist = data.new
      this.initSections()
      this.$refs['checklistModal'].show()
    },
    handleChecklistOk(bvModalEvt){
      bvModalEvt.preventDefault();
      this.handleChecklistSubmit()  
    },
    handleChecklistSubmit(){
        let axiosMethod = this.newChecklist ? this.$axios.$post : this.$axios.$put
        axiosMethod('checklist/', this.checklist, { headers: ""})
        .then(res => {
          let newcheck = this.checklists.map( section => {
            if(section.id === res.section){
              section.checklists.push(res)
            }
          })
          this.$refs['checklistModal'].hide()
        })
        .catch(err => console.log(err))      
    },
    getChecklists(){           
      this.options.sections.options = [{ value: null, text: "Select a City"}]  
      this.$axios.$get('checklist/section/all', { headers: ""})
      .then(res => this.checklists = res )     
    }
  },
  mounted() {
      this.getChecklists()
  }
}
</script>
