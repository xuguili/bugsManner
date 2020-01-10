import axios from 'axios';
import ElementUI from 'element-ui'
import qs from 'qs'

axios.defaults.withCredentials=true
axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';
let base = 'http://localhost:5000';


axios.interceptors.response.use(data =>{
    const code = data.data.code;
    const msg = data.data.msg;
    if(code == -1){ //未登录
        sessionStorage.removeItem('user');
        ElementUI.Message({
            message:msg,
            type:'error'
        });
        this.$router.push('/login');
    }
    return data;
},error => {
    return Promise.reject(error)
})

//登录
export const requestLogin = params => { return axios.post(`${base}/login`, qs.stringify(params)).then(res => res.data); };
//退出登录post
export const requestLogout = params => { return axios.post(`${base}/logout`, params).then(res => res.data); };
//获取用户名
export const getUserName = params => { return axios.get(`${base}/getUserInfo`, {params}).then(res => res.data); };

//需求列表get
export const listNeed = params => { return axios.get(`${base}/need/list`, {params}).then(res => res.data); };
//新增需求
export const addNeed = params => { return axios.post(`${base}/need/add`, qs.stringify(params)).then(res => res.data); };
//更新需求
export const editNeed = params => { return axios.post(`${base}/need/update`, qs.stringify(params)).then(res => res.data); };
//删除需求
export const deleteNeed = params => { return axios.get(`${base}/need/delete`, {params}).then(res => res.data); };
//批量删除需求
export const batchDeleteNeed = params => { return axios.get(`${base}/need/batchDelete`, {params}).then(res => res.data); };

//缺陷列表get
export const listBug = params => { return axios.get(`${base}/bug/listBugs`, {params}).then(res => res.data); };
//新增缺陷
export const addBug = params => { return axios.post(`${base}/bug/addBugs`, qs.stringify(params)).then(res => res.data); };
//更新缺陷
export const editBug = params => { return axios.post(`${base}/bug/updateBugs`, qs.stringify(params)).then(res => res.data); };
//删除缺陷
export const deleteBug = params => { return axios.get(`${base}/bug/deleteBugs`, {params}).then(res => res.data); };
//批量删除缺陷
export const batchDeleteBug = params => { return axios.get(`${base}/bug/batchDeleteBugs`, {params}).then(res => res.data); };

//统计缺陷
export const statisticBug = params => { return axios.get(`${base}/bug/statistic`, {params}).then(res => res.data); };


//迭代列表get
export const listIter = params => { return axios.get(`${base}/iteration/listIters`, {params}).then(res => res.data); };
//新增迭代
export const addIter = params => { return axios.post(`${base}/iteration/addIters`, qs.stringify(params)).then(res => res.data); };
//更新迭代
export const editIter= params => { return axios.post(`${base}/iteration/updateIters`, qs.stringify(params)).then(res => res.data); };
//删除迭代
export const deleteIter = params => { return axios.get(`${base}/iteration/deleteIters`, {params}).then(res => res.data); };
//批量删除迭代
export const batchDeleteIter = params => { return axios.get(`${base}/iteration/batchDeleteIters`, {params}).then(res => res.data); };


//报告列表get
export const listReport = params => { return axios.get(`${base}/reportForms/report`, {params}).then(res => res.data); };
//新增报告
export const addReport = params => { return axios.post(`${base}/reportForms/report/addReport`, qs.stringify(params)).then(res => res.data); };
//更新报告
export const editReport= params => { return axios.post(`${base}/reportForms/report/editReport`, qs.stringify(params)).then(res => res.data); };
//获取报告信息
export const getReport = params => {return axios.get(`${base}/reportForms/report/view`, {params: params }).then(res => res.data);};
//删除报告
export const deleteReport = params => { return axios.get(`${base}/reportForms/report/deleteReport`, {params}).then(res => res.data); };
//批量删除报告
export const batchDeleteReport = params => { return axios.get(`${base}/reportForms/report/batchDeleteReport`, {params}).then(res => res.data); };
