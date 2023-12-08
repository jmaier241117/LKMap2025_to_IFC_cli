select a.T_Ili_Tid, p.T_Ili_Tid as id , aa.dispName from abstichpunkt as a
left join lkpunkt as p on a.lkpunktref = p.T_Id
left join abstichpunkt_art as aa on a.art = aa.T_Id
WHERE p.T_Id is not null
