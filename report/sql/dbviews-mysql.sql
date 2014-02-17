
/* vw_user_balance DB View */
create or replace view vw_user_balance as 
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, 
  (case when (Upper(usr.username) like '%KAXA%') or (Upper(usr.username) like '%CAJA%') then (usrprf.balance-(25*60))/60 else (usrprf.balance-(10*60))/60 end) as balance_tot
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
where usr.is_active=1
order by area.name, usr.username;
/*limit 100*/

/* vw_transf_balance DB View */
create or replace view vw_transf_balance as
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, sum(trf.credits)/60 as transf_payee, 0 as transf_debtor, 0 as balance_tot
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join serv_transfer trf on (trf.credits_payee_id=usr.id)
where (trf.credits!=0) and (trf.status!='r')
group by area.name, usr.username
union
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, 0 as transf_payee, -(sum(trf.credits)/60) as transf_debtor, 0 as balance_tot
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join serv_transfer trf on (trf.credits_debtor_id=usr.id)
where (trf.credits!=0) and (trf.status!='r')
group by area.name, usr.username
union
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, 0 as transf_payee, 0 as transf_debtor, sum(usrbal.balance_tot) as balance_tot
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join vw_user_balance usrbal on usrbal.user_id=usr.id
where (usrbal.balance_tot is not null)
group by area.name, usr.username
order by 2,4;
/*limit 100*/

/* vw_transf_balance_check DB View */
create or replace view vw_transf_balance_check as
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, 
  sum(trfbal.transf_payee) as transf_payee, sum(trfbal.transf_debtor) as transf_debtor, sum(trfbal.balance_tot) as balance_tot, (sum(trfbal.transf_payee)+sum(trfbal.transf_debtor))-sum(trfbal.balance_tot) as balance_check
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join vw_transf_balance trfbal on trfbal.user_id=usr.id
group by area.name, usr.username
having (sum(trfbal.transf_payee)!=0) or (sum(trfbal.transf_debtor)!=0) or (sum(trfbal.balance_tot)!=0)
order by area.name, usr.username;
/*limit 100*/

/* vw_serv_transf_ DB View */
create or replace view vw_serv_transf as
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, svc.id as serv_id, svc.description as serv_desc, svc.is_offer, svc.is_active,
  trf.id as transf_id, usr_tcd.username as transf_user, trf.status as transf_status, trf.request_date as transf_request, trf.confirmation_date as transf_confirm,
  (trf.credits)/60 as transf_payee, 0 as transf_payee_sum, 0 as transf_debtor, 0 as transf_debtor_sum
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join serv_service svc on svc.creator_id=usr.id
left join serv_transfer trf on trf.service_id=svc.id
left join auth_user usr_tcd on usr_tcd.id=trf.credits_debtor_id
where (trf.credits!=0) and (trf.status!='r') and (usr_tcd.id!=usr.id)
union
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, svc.id as serv_id, svc.description as serv_desc, svc.is_offer, svc.is_active,
  trf.id as transf_id, count(usr_tcd.username) as transf_user, trf.status as transf_status, trf.request_date as transf_request, trf.confirmation_date as transf_confirm,
  0 as transf_payee, sum(trf.credits)/60 as transf_payee_sum, 0 as transf_debtor, 0 as transf_debtor_sum
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join serv_service svc on svc.creator_id=usr.id
left join serv_transfer trf on trf.service_id=svc.id
left join auth_user usr_tcd on usr_tcd.id=trf.credits_debtor_id
where (trf.credits!=0) and (trf.status!='r') and (usr_tcd.id!=usr.id)
group by area.name, usr.username, svc.id
having count(usr_tcd.username)>1
union
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, svc.id as serv_id, svc.description as serv_desc, svc.is_offer, svc.is_active,
  trf.id as transf_id, usr_tcp.username as transf_user, trf.status as transf_status, trf.request_date as transf_request, trf.confirmation_date as transf_confirm,
  0 transf_payee, 0 as transf_payee_sum, -(trf.credits)/60 as transf_debtor, 0 as transf_debtor_sum
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join serv_service svc on svc.creator_id=usr.id
left join serv_transfer trf on trf.service_id=svc.id
left join auth_user usr_tcp on usr_tcp.id=trf.credits_payee_id
where (trf.credits!=0) and (trf.status!='r') and (usr_tcp.id!=usr.id)
union
select area.id as area_id, area.name as area_name, usr.id as user_id, usr.username as user_name, svc.id as serv_id, svc.description as serv_desc, svc.is_offer, svc.is_active,
  trf.id as transf_id, count(usr_tcp.username) as transf_user, trf.status as transf_status, trf.request_date as transf_request, trf.confirmation_date as transf_confirm,
  0 transf_payee, 0 as transf_payee_sum, 0 as transf_payee, sum(-trf.credits)/60 as transf_debtor_sum
from serv_area area
left join user_profile usrprf on usrprf.area_id=area.id
left join auth_user usr on usr.id=usrprf.user_ptr_id
left join serv_service svc on svc.creator_id=usr.id
left join serv_transfer trf on trf.service_id=svc.id
left join auth_user usr_tcp on usr_tcp.id=trf.credits_payee_id
where (trf.credits!=0) and (trf.status!='r') and (usr_tcp.id!=usr.id)
group by area.name, usr.username, svc.id
having count(usr_tcp.username)>1
order by 2, 4, 6;
/*limit 100*/
