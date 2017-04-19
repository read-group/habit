delete FROM schoolerp.account_accounthistory;
update account_account set balance=0;
delete FROM feedback_post;
delete From feedback_feedback;
delete FROM schoolerp.feedback_orgactivityhistory;
update  schoolerp.activity_activity set applyNumber=0;
