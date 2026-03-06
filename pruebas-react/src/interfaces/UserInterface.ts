export interface User {
  UserName: String;
  Password: String;
  isLoged:boolean;
}


export const mockUsers: User[] = [
  { UserName: "admincentral", Password: "SafePassword123", isLoged: false },
  { UserName: "lucia_dev", Password: "dev_mode_on_2024", isLoged: false },
  { UserName: "marcos_perez", Password: "Password99", isLoged: false },
  { UserName: "sofia.garcia", Password: "User_Secret_88", isLoged: false },
  { UserName: "tech_support", Password: "Support#Access!", isLoged: false },
  { UserName: "juan_moya", Password: "Juanito_Pass_10", isLoged: false },
  { UserName: "elena_marketing", Password: "Mkt_Strong_Pass", isLoged: false },
  { UserName: "guest_user", Password: "GuestAccess01", isLoged: false },
  { UserName: "roberto_hr", Password: "HR_Manager_2025", isLoged: false },
  { UserName: "ana_analyst", Password: "Data_Is_Power_1", isLoged: false }
];