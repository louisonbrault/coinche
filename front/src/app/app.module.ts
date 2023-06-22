import { DatePipe } from '@angular/common';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GameComponent } from './game/game.component';
import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { fr_FR } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import fr from '@angular/common/locales/fr';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { NzAvatarModule } from 'ng-zorro-antd/avatar';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzCardModule } from 'ng-zorro-antd/card';
import { NzDatePickerModule } from 'ng-zorro-antd/date-picker';
import { NzDividerModule } from 'ng-zorro-antd/divider';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzGridModule } from 'ng-zorro-antd/grid';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzImageModule } from 'ng-zorro-antd/image';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzInputNumberModule } from 'ng-zorro-antd/input-number';
import { NzNotificationModule } from 'ng-zorro-antd/notification';
import { NzRadioModule } from 'ng-zorro-antd/radio';
import { NzRateModule } from 'ng-zorro-antd/rate';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzTableModule } from 'ng-zorro-antd/table';
import { GameListComponent } from './game-list/game-list.component';
import { HeaderComponent } from './header/header.component';

import { SocialLoginModule, SocialAuthServiceConfig } from '@abacritt/angularx-social-login';
import {  FacebookLoginProvider } from '@abacritt/angularx-social-login';
import { CoolSocialLoginButtonsModule } from '@angular-cool/social-login-buttons';
import { SubHeaderComponent } from './sub-header/sub-header.component';
import { NewGameComponent } from './new-game/new-game.component';

import { StoreModule } from '@ngrx/store';
import { authReducer } from './auth/auth.reducer';
import { ScoreBoardComponent } from './score-board/score-board.component';
import { ProfileComponent } from './profile/profile.component';

registerLocaleData(fr);

@NgModule({
  declarations: [
    AppComponent,
    GameComponent,
    GameListComponent,
    HeaderComponent,
    SubHeaderComponent,
    NewGameComponent,
    ScoreBoardComponent,
    ProfileComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    NzAvatarModule,
    NzButtonModule,
    NzCardModule,
    NzDatePickerModule,
    NzDividerModule,
    NzFormModule,
    NzGridModule,
    NzIconModule,
    NzImageModule,
    NzInputModule,
    NzInputNumberModule,
    NzNotificationModule,
    NzRadioModule,
    NzRateModule,
    NzSelectModule,
    NzTableModule,
    SocialLoginModule,
    CoolSocialLoginButtonsModule,
    StoreModule.forRoot({ auth: authReducer })
  ],
  providers: [
    DatePipe,
    { provide: NZ_I18N, useValue: fr_FR },
    {
      provide: 'SocialAuthServiceConfig',
      useValue: {
        autoLogin: false,
        providers: [
          {
            id: FacebookLoginProvider.PROVIDER_ID,
            provider: new FacebookLoginProvider('499426098996343')
          }
        ],
        onError: (err) => {
          console.error(err);
        }
      } as SocialAuthServiceConfig,
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
