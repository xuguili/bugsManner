import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import Main from './views/Main.vue'
import Need from './views/need/Need.vue'
import addNeed from './views/need/Need.vue'
import Bug from './views/bug/Bug.vue'
import addBug from './views/bug/Bug.vue'
import BugStatus from './views/reportforms/BugStatus.vue'
import BugHandler from './views/reportforms/BugHandler.vue'
import BugCreater from './views/reportforms/BugCreater.vue'
import BugTrend from './views/reportforms/BugTrend.vue'
import Iteration from './views/iteration/Iteration.vue'
import addIter from './views/iteration/Iteration.vue'
import Report from './views/reportforms/report/Report.vue'
import addTestReport from './views/reportforms/report/addTestReport.vue'
import addReleaseReport from './views/reportforms/report/addReleaseReport.vue'
import editTestReport from './views/reportforms/report/editTestReport.vue'
import editReleaseReport from './views/reportforms/report/editReleaseReport.vue'
import viewTestReport from './views/reportforms/report/viewTestReport.vue'
import viewReleaseReport from './views/reportforms/report/viewReleaseReport.vue'


let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
     {
        path: '/',
        component: Home,
        name: '',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            { path: '/main', component: Main, name: '', hidden: true },
        ]
    },
    {
        path: '/',
        component: Home,
        name: '需求',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            { path: '/need/list/:type', component: Need, name: '需求列表' },
            { path: '/addNeed', component:addNeed, name:'新增需求'}
        ]
    },
    {
        path: '/',
        component: Home,
        name: '迭代',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            { path: '/iteration/listIter/:type', component: Iteration, name: '迭代列表' },
            { path: '/addIter', component:addIter, name:'新增迭代'}
        ]
    },
    {
        path: '/',
        component: Home,
        name: '缺陷',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            { path: '/bug/listBugs/:type', component: Bug, name: '缺陷列表' },
            { path: '/addBug', component:addBug, name:'新增缺陷'}
        ]
    },
    {
        path: '/',
        component: Home,
        name: '报表',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            { path: '/reportforms/BugStatus', component: BugStatus, name: '缺陷状态分布图' },
            { path: '/reportforms/BugTrend', component: BugTrend, name: '缺陷日趋势图' },
            { path: '/reportforms/BugCreater', component: BugCreater, name: '缺陷创建人分布图' },
            { path: '/reportforms/BugHandler', component: BugHandler, name: '缺陷处理人分布图' },
            { path: '/reportforms/report/:type', component: Report, name: '报告列表' },
            { path: '/addTestReport', component: addTestReport, name: '新增测试报告' },
            { path: '/addReleaseReport', component: addReleaseReport, name: '新增发布报告' },
            { path: '/editTestReport', component: editTestReport, name: '编辑测试报告' },
            { path: '/editReleaseReport', component: editReleaseReport, name: '编辑发布报告' },
            { path: '/viewTestReport', component: viewTestReport, name: '预览测试报告' },
            { path: '/viewReleaseReport', component: viewReleaseReport, name: '预览发布报告' },

        ]
    },
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }

];

export default routes;