<template>
  <v-sheet id="scrolling-techniques-7" class="overflow-y-auto" max-height="875">
    <!-- background-color: red; -->
    <v-container style="margin-top: 64px; height: 1500px; width: 950px">
      <div class="dataProcessing" style="margin: 60px">
        <div class="chartLong d-flex justify-center" style="margin: 60px">
          <h2
            class="d-flex justify-start"
            style="margin-bottom: 20px; margin-right: 30px"
          >
            กราฟเเสดงข้อมูลท่าทางกรากระทำของนักเรียนประจำวัน
          </h2>
          <ChartLong />
        </div>
        <div class="chartLongAll d-flex justify-center" style="margin: 60px">
          <h2 class="" style="margin-bottom: 20px">
            กราฟเเสดงข้อมูลท่าทางกรากระทำของนักเรียนทั้งหมด
          </h2>
          <ChartLongAll />
        </div>
        <div class="table">
          <h2 class="d-flex justify-start" style="margin-bottom: 20px">
            ตารางเเสดงข้อมูลท่าทางกรากระทำของนักเรียน
          </h2>
          <Table />
        </div>
      </div>
    </v-container>
  </v-sheet>
</template>

<script>
// @ is an alias to /src
import Table from "@/components/Table.vue";
import ChartLongAll from "@/components/ChartLongAll.vue";
import ChartLong from "@/components/ChartLong.vue";

export default {
  name: "DataProcessing",
  components: {
    Table,
    ChartLongAll,
    ChartLong,
  },
  beforeCreate() {
    if (!this.$session.exists()) {
      this.$router.push("/");
    }
  },
};
</script>
