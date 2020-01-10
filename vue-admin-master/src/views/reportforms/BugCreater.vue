<template>
    <section  >
         <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
		    <el-form :inline="true" :model="filters">
                <el-form-item label="创建时间">
                        <el-date-picker v-model="filters.startDate" type="date" placeholder="开始日期"
                                        :options="startDateOption" @on-change="onStartDateChange">
                        </el-date-picker>
                        <el-date-picker v-model="filters.endDate" type="date" placeholder="结束日期"
                        :options="endDateOption" @on-change="onEndDateChange">
                        </el-date-picker>
                </el-form-item>
				<el-form-item>
					<el-button type="primary" size="medium" icon="el-icon-search" v-on:click="search">生成报表</el-button>
				</el-form-item>
			</el-form>
        </el-col>
        <el-row class="chart-container" align="center">
            <el-col :span="12">
                <div id="chartColumn" style="width:100%; height:300px;"></div>
            </el-col>
<!--            <el-col :span="24">-->
<!--                <a href="http://echarts.baidu.com/examples.html" target="_blank" style="float: right;">more>></a>-->
<!--            </el-col>-->
        </el-row>
        <el-table :data="createrList" highlight-current-row v-loading="listLoading"  style="width: 50%;" align="center">
            <el-table-column prop="creater_name" label="状态" width="300"></el-table-column>
            <el-table-column prop="creater_bug" label="小计" width="300"></el-table-column>
        </el-table>
    </section>
</template>

<script>
    import { statisticBug } from "../../api/api.js";
    import util from "../../common/js/util";
    import echarts from 'echarts'

    export default {
        data() {
            return {
                filters:{
                    startDate:'',
                    endDate:''
                },
                startDateOption:{},
                endDateOption:{},
                chartColumn: null,
                listLoading:false,
                createrList:[],
            }
        },

        methods: {
            onStartDateChange(startDate, type) {
                this.endDateOption = {
                    disabledDate(endDate) {
                        return endDate < new Date(startDate) || endDate > Date.now()
                    }
                }
            },

            onEndDateChange(endDate, type) {
                this.startDateOption = {
                    disabledDate(startDate) {
                        return startDate > new Date(endDate) || startDate > Date.now()
                    }
                }
            },
            search() {
                this.statisticBug();
            },
            statisticBug() {
                let bugParams = {
                    startDate: this.filters.startDate ? util.formatDate.format(new Date(this.filters.startDate), 'yyyy-MM-dd') : '',
                    endDate: this.filters.endDate ? util.formatDate.format(new Date(this.filters.endDate), 'yyyy-MM-dd') : '',
                }
                statisticBug(bugParams).then((res) => {
                    this.creater_name = res.creater_name;
                    this.creater_bug = res.creater_bug;
                    this.drawColumnChart(res.creater_name, res.creater_bug);
                    this.createrList = res.createrList;
                    this.listLoading = false;
                });
            },

            drawColumnChart(creater_name, creater_bug) {
                this.chartColumn = echarts.init(document.getElementById('chartColumn'));
                this.chartColumn.setOption({
                    title: {text: '缺陷创建人分布图'},
                    tooltip: {},
                    xAxis: {
                        // data: ["徐", "尹", "李", "肖"]
                        data: creater_name
                    },
                    yAxis: {},
                    series: [{
                        name: '缺陷数',
                        type: 'bar',
                        // data: [5, 20, 36, 10]
                        data: creater_bug
                    }]
                });
            }
        },

        mounted: function () {
            this.statisticBug();

        }
    }
</script>

<style scoped>
    .chart-container {
        width: 100%;
        height: 100%;
        float: left;
    }
    /*.chart div {
        height: 400px;
        float: left;
    }*/

    .el-col {
        padding: 30px 20px;
    }
</style>
