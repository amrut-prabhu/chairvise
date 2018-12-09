<template>
  <div>
    <h1 
      v-show="!text.edit"
      title="Click to edit!"
      @click="toggleEdit(this, text)">{{ text.val }}</h1>
    <el-input 
      v-show="text.edit"
      v-model="text.val"
      type="textarea"
      autosize
      style="width: 85%"
      @blur="saveEdit(this, text)"/>
  </div>
</template>

<script>
export default {
  name: "EditableHeader",
  props: ["text"],
  data() {
    return {
      title: "Editable Header Inside."
    };
  },
  methods: {
    toggleEdit: function(ev, text) {
      text.edit = !text.edit;
      // if (text.edit) {
      // 	Vue.nextTick(function() {
      // 		ev.$$.input.focus();
      // 	})
      // }
    },
    saveEdit: function(ev, text) {
      //save your changes
      this.toggleEdit(ev, text);
      this.$emit("update:text", text);
    }
  }
};
</script>