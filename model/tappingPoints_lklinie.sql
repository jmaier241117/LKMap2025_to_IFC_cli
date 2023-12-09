select  a.T_Ili_Tid, l.T_Ili_Tid as id,  aa.dispName  from abstichpunkt as a
left join lklinie as l on a.lklinieref = l.T_Id
left join abstichpunkt_art as aa on a.art = aa.T_Id
WHERE l.T_Id is not null